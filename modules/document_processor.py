"""
Document Processing & Ingestion Module for LegalDocAiAssist.

Handles multi-format document ingestion:
- Digital PDF via PyMuPDF (fitz) with page preservation
- Scanned PDF fallback via Gemini Multimodal OCR
- Word documents via python-docx with heading preservation
- Document images (JPG, JPEG, PNG) via Gemini Multimodal OCR
- Safe legal text cleaning preserving all critical qualifiers and negations
"""

import os
import io
import re
from typing import List, Dict, Any, Optional, Union

# Optional third-party imports with graceful detection
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

# Import Gemini client utilities
from modules.rag import get_gemini_client, resolve_api_key, resolve_model_name, HAS_GENAI_SDK


def clean_legal_text(text: str) -> str:
    """
    Cleans raw document text while strictly preserving legal meaning.
    - Normalizes unicode whitespace and quotation marks
    - Removes unprintable control characters
    - Normalizes excessive blank lines while preserving paragraph breaks
    - NEVER alters or drops legal qualifiers (not, shall, must, unless, except, etc.)
    """
    if not text:
        return ""

    # Replace common typographic characters with clean standard equivalents
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "--",
        "\u00a0": " ",  # non-breaking space
        "\ufeff": "",   # BOM
        "\r\n": "\n",
        "\r": "\n",
    }
    for orig, target in replacements.items():
        text = text.replace(orig, target)

    # Remove non-printable control characters except standard whitespace
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Normalize horizontal whitespace (spaces, tabs) without merging lines
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    
    # Remove excessive blank lines (> 2 consecutive empty lines)
    cleaned_lines: List[str] = []
    consecutive_empty = 0
    for line in lines:
        if not line:
            consecutive_empty += 1
            if consecutive_empty <= 2:
                cleaned_lines.append("")
        else:
            consecutive_empty = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def extract_from_pdf(
    file_input: Union[str, bytes, io.BytesIO],
    gemini_api_key: Optional[str] = None,
    gemini_model: Optional[str] = None,
    min_char_threshold_per_page: int = 40
) -> List[Dict[str, Any]]:
    """
    Extracts text from a PDF file using PyMuPDF.
    Preserves page numbers. If text is missing or sparse, triggers Gemini Multimodal OCR fallback.
    """
    if not HAS_PYMUPDF:
        # Fallback 1: Try pypdf if installed
        raw_bytes = b""
        if isinstance(file_input, str) and os.path.exists(file_input):
            with open(file_input, "rb") as f:
                raw_bytes = f.read()
        elif isinstance(file_input, bytes):
            raw_bytes = file_input
        elif hasattr(file_input, "read"):
            raw_bytes = file_input.read()
            if hasattr(file_input, "seek"):
                file_input.seek(0)

        if HAS_PYPDF and raw_bytes:
            try:
                reader = pypdf.PdfReader(io.BytesIO(raw_bytes))
                pdf_sections = []
                for p_idx, p in enumerate(reader.pages):
                    p_txt = p.extract_text() or ""
                    cleaned = clean_legal_text(p_txt)
                    pdf_sections.append({
                        "text": cleaned,
                        "page": p_idx + 1,
                        "section": f"Page {p_idx + 1}",
                        "source_type": "digital_pdf",
                        "is_ocr": False
                    })
                if any(len(s["text"]) > 10 for s in pdf_sections):
                    return pdf_sections
            except Exception:
                pass

        # Fallback 2: Pure-Python stream parser for uncompressed/standard PDF text streams
        if raw_bytes:
            try:
                streams = re.findall(b'stream\r?\n(.*?)\r?\nendstream', raw_bytes, re.DOTALL)
                if streams:
                    stream_sections = []
                    for s_idx, s_data in enumerate(streams):
                        decoded = s_data.decode("latin1", errors="replace")
                        line_matches = re.findall(r'\((.*?)\)\s*(?:[\'Tj]|\bTJ\b)', decoded)
                        if line_matches:
                            # Clean escaped parentheses
                            cleaned_lines = [m.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\") for m in line_matches]
                            cleaned = clean_legal_text("\n".join(cleaned_lines))
                            if cleaned:
                                stream_sections.append({
                                    "text": cleaned,
                                    "page": s_idx + 1,
                                    "section": f"Page {s_idx + 1}",
                                    "source_type": "digital_pdf",
                                    "is_ocr": False
                                })
                    if stream_sections:
                        return stream_sections
            except Exception:
                pass

        raise ImportError("PyMuPDF (fitz) is not installed. Please install it via requirements.txt.")

    doc = None
    if isinstance(file_input, str):
        doc = fitz.open(file_input)
    elif isinstance(file_input, bytes):
        doc = fitz.open(stream=file_input, filetype="pdf")
    elif hasattr(file_input, "read"):
        content = file_input.read()
        doc = fitz.open(stream=content, filetype="pdf")
        if hasattr(file_input, "seek"):
            file_input.seek(0)
    else:
        raise ValueError("Unsupported PDF input type.")

    sections: List[Dict[str, Any]] = []
    total_extracted_chars = 0
    pages_to_ocr: List[int] = []

    for page_idx, page in enumerate(doc):
        page_num = page_idx + 1
        page_text = page.get_text("text").strip()
        cleaned = clean_legal_text(page_text)
        total_extracted_chars += len(cleaned)

        if len(cleaned) < min_char_threshold_per_page:
            pages_to_ocr.append(page_idx)

        sections.append({
            "text": cleaned,
            "page": page_num,
            "section": f"Page {page_num}",
            "source_type": "digital_pdf",
            "is_ocr": False
        })

    # If the document has pages with virtually no text, attempt Gemini multimodal OCR
    if pages_to_ocr and HAS_GENAI_SDK:
        resolved_key = resolve_api_key(gemini_api_key)
        if resolved_key:
            try:
                client = get_gemini_client(api_key=resolved_key)
                model_name = resolve_model_name(gemini_model)

                for page_idx in pages_to_ocr:
                    page = doc[page_idx]
                    page_num = page_idx + 1
                    # Render page as high-res pixmap
                    pix = page.get_pixmap(dpi=200)
                    img_bytes = pix.tobytes("png")
                    
                    ocr_text = _gemini_ocr_image_bytes(
                        client=client,
                        model_name=model_name,
                        image_bytes=img_bytes,
                        mime_type="image/png"
                    )
                    
                    if ocr_text and len(ocr_text.strip()) > len(sections[page_idx]["text"]):
                        sections[page_idx]["text"] = clean_legal_text(ocr_text)
                        sections[page_idx]["source_type"] = "scanned_pdf"
                        sections[page_idx]["is_ocr"] = True
            except Exception as ocr_err:
                # Log or keep digital text fallback if OCR fails
                pass

    doc.close()
    return sections


def extract_from_docx(
    file_input: Union[str, bytes, io.BytesIO]
) -> List[Dict[str, Any]]:
    """
    Extracts text from a DOCX file preserving headings, paragraphs, and tables.
    """
    if not HAS_DOCX:
        raise ImportError("python-docx is not installed. Please install it via requirements.txt.")

    doc_stream = file_input
    if isinstance(file_input, bytes):
        doc_stream = io.BytesIO(file_input)
    elif hasattr(file_input, "read") and not hasattr(file_input, "seek"):
        doc_stream = io.BytesIO(file_input.read())

    doc = docx.Document(doc_stream)
    sections: List[Dict[str, Any]] = []
    current_heading = "General"
    current_paragraphs: List[str] = []

    def flush_section():
        nonlocal current_paragraphs
        if current_paragraphs:
            combined_text = "\n\n".join(current_paragraphs).strip()
            cleaned = clean_legal_text(combined_text)
            if cleaned:
                sections.append({
                    "text": cleaned,
                    "page": 1,  # DOCX doesn't have fixed pagination
                    "section": current_heading,
                    "source_type": "docx",
                    "is_ocr": False
                })
            current_paragraphs = []

    # Iterate through body elements (paragraphs and tables)
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue

        # Check if paragraph is a heading
        style_name = p.style.name if p.style else ""
        if "Heading" in style_name or p.style.name.startswith("Title"):
            flush_section()
            current_heading = text
        else:
            current_paragraphs.append(text)

    # Process tables in the docx
    for table in doc.tables:
        flush_section()
        table_rows = []
        for row in table.rows:
            row_cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            if any(row_cells):
                table_rows.append(" | ".join(row_cells))
        if table_rows:
            table_text = "\n".join(table_rows)
            sections.append({
                "text": clean_legal_text(table_text),
                "page": 1,
                "section": f"{current_heading} (Table)",
                "source_type": "docx_table",
                "is_ocr": False
            })

    flush_section()
    return sections


def extract_from_image(
    file_input: Union[str, bytes, io.BytesIO],
    mime_type: str = "image/png",
    gemini_api_key: Optional[str] = None,
    gemini_model: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Extracts text from a standalone document image (JPG, JPEG, PNG) using Gemini Multimodal OCR.
    """
    if not HAS_PILLOW:
        raise ImportError("Pillow is not installed. Please install it via requirements.txt.")

    # Read image bytes
    if isinstance(file_input, str):
        with open(file_input, "rb") as f:
            image_bytes = f.read()
    elif isinstance(file_input, bytes):
        image_bytes = file_input
    elif hasattr(file_input, "read"):
        image_bytes = file_input.read()
        if hasattr(file_input, "seek"):
            file_input.seek(0)
    else:
        raise ValueError("Unsupported image input type.")

    # Verify image integrity via Pillow
    image = Image.open(io.BytesIO(image_bytes))
    image.verify()

    resolved_key = resolve_api_key(gemini_api_key)
    if not resolved_key:
        raise ValueError("GEMINI_API_KEY is required for image and scanned document OCR.")

    client = get_gemini_client(api_key=resolved_key)
    model_name = resolve_model_name(gemini_model)

    ocr_text = _gemini_ocr_image_bytes(
        client=client,
        model_name=model_name,
        image_bytes=image_bytes,
        mime_type=mime_type
    )

    cleaned = clean_legal_text(ocr_text)
    return [{
        "text": cleaned,
        "page": 1,
        "section": "Document Image OCR",
        "source_type": "image_ocr",
        "is_ocr": True
    }]


def _gemini_ocr_image_bytes(
    client: Any,
    model_name: str,
    image_bytes: bytes,
    mime_type: str
) -> str:
    """Helper to send image bytes to Gemini Multimodal for legal text OCR."""
    from google.genai import types

    prompt = (
        "You are an expert legal document transcription engine. "
        "Transcribe all text from this legal document image with 100% fidelity. "
        "Strictly preserve:\n"
        "- All clause numbers, section headers, and subclauses\n"
        "- Exact legal wording, including words like 'shall', 'must', 'not', 'unless', 'except'\n"
        "- Numerical values, dates, percentages, amounts, and party names\n"
        "- Table formatting if present\n"
        "Do NOT summarize, do NOT omit any text, and do NOT add commentary. Return only the extracted text."
    )

    contents = [
        types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        ),
        prompt,
    ]

    response = client.models.generate_content(
        model=model_name,
        contents=contents
    )

    return response.text.strip() if hasattr(response, "text") and response.text else ""


def extract_from_text_file(
    file_input: Union[str, bytes, io.BytesIO]
) -> List[Dict[str, Any]]:
    """
    Extracts and structures plain text (.txt, .md) documents into logical page sections.
    """
    if isinstance(file_input, str):
        if os.path.exists(file_input):
            with open(file_input, "r", encoding="utf-8", errors="replace") as f:
                raw_text = f.read()
        else:
            raw_text = file_input
    elif isinstance(file_input, bytes):
        raw_text = file_input.decode("utf-8", errors="replace")
    elif hasattr(file_input, "read"):
        content = file_input.read()
        if isinstance(content, bytes):
            raw_text = content.decode("utf-8", errors="replace")
        else:
            raw_text = str(content)
        if hasattr(file_input, "seek"):
            file_input.seek(0)
    else:
        raise ValueError("Unsupported text input type.")

    cleaned = clean_legal_text(raw_text)
    paragraphs = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
    sections: List[Dict[str, Any]] = []
    current_page = 1
    current_text: List[str] = []
    word_count = 0

    for p in paragraphs:
        current_text.append(p)
        word_count += len(p.split())
        if word_count >= 350:
            sections.append({
                "text": "\n\n".join(current_text),
                "page": current_page,
                "section": f"Page {current_page}",
                "source_type": "text_document",
                "is_ocr": False
            })
            current_page += 1
            current_text = []
            word_count = 0

    if current_text:
        sections.append({
            "text": "\n\n".join(current_text),
            "page": current_page,
            "section": f"Page {current_page}",
            "source_type": "text_document",
            "is_ocr": False
        })

    return sections or [{
        "text": cleaned,
        "page": 1,
        "section": "Page 1",
        "source_type": "text_document",
        "is_ocr": False
    }]


def process_document(
    file_input: Any,
    file_name: str,
    gemini_api_key: Optional[str] = None,
    gemini_model: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Main entry point for document ingestion.
    Inspects file extension and dispatches to appropriate extractor.
    Returns list of section dicts: [{'text', 'page', 'section', 'source_type', 'is_ocr', 'file_name'}].
    """
    ext = os.path.splitext(file_name)[1].lower()

    if ext == ".pdf":
        sections = extract_from_pdf(
            file_input,
            gemini_api_key=gemini_api_key,
            gemini_model=gemini_model
        )
    elif ext in [".docx", ".doc"]:
        sections = extract_from_docx(file_input)
    elif ext in [".txt", ".text", ".md"]:
        sections = extract_from_text_file(file_input)
    elif ext in [".png", ".jpg", ".jpeg"]:
        mime_type = "image/png" if ext == ".png" else "image/jpeg"
        sections = extract_from_image(
            file_input,
            mime_type=mime_type,
            gemini_api_key=gemini_api_key,
            gemini_model=gemini_model
        )
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Supported formats: PDF, DOCX, TXT, MD, JPG, JPEG, PNG.")

    for s in sections:
        s["file_name"] = file_name

    return sections


def _split_oversized_text(
    text: str,
    max_chars: int = 1200,
    overlap_chars: int = 150
) -> List[str]:
    """
    Splits an oversized clause cleanly by sentence or paragraph boundaries.
    Preserves legal words and context continuity.
    """
    if len(text) <= max_chars:
        return [text]

    # Split by sentence boundaries: . ! ? followed by whitespace or newline
    sentence_end_pattern = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_end_pattern.split(text)

    chunks: List[str] = []
    current_chunk = ""

    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue

        if not current_chunk:
            current_chunk = s_clean
        elif len(current_chunk) + len(s_clean) + 1 <= max_chars:
            current_chunk += " " + s_clean
        else:
            chunks.append(current_chunk)
            # Add small overlap from previous chunk if possible
            overlap_prefix = current_chunk[-overlap_chars:] if len(current_chunk) > overlap_chars else ""
            if overlap_prefix and " " in overlap_prefix:
                overlap_prefix = overlap_prefix.split(" ", 1)[-1]
                current_chunk = f"{overlap_prefix} {s_clean}".strip()
            else:
                current_chunk = s_clean

    if current_chunk:
        chunks.append(current_chunk)

    return chunks if chunks else [text]


def chunk_document_sections(
    sections: List[Dict[str, Any]],
    max_chars: int = 1200,
    overlap_chars: int = 150
) -> List[Dict[str, Any]]:
    """
    Clause-aware chunker that respects legal document hierarchy:
    - Numbered sections, articles, and clauses (e.g. '8. Termination', '8.2', 'Clause 3(a)')
    - Metadata schema per specification:
      {
        "chunk_id": "doc_chunk_1",
        "text": "...",
        "page": 4,
        "section": "8. Termination",
        "clause": "8.2",
        "source": "uploaded_document",
        "file_name": "contract.pdf"
      }
    - Ensures legal negation words and qualifiers are strictly preserved.
    """
    chunks: List[Dict[str, Any]] = []
    chunk_counter = 1

    # Structural regex patterns for legal headers & clauses
    section_patterns = [
        re.compile(r'^(?:SECTION|ARTICLE|CLAUSE)\s+([0-9IVXLCDM]+(?:\.[0-9]+)*)[:\.\-\s]*(.*)', re.IGNORECASE),
        re.compile(r'^([0-9]{1,2})\.\s+([A-Z][A-Za-z0-9\s,\-_/]{2,50})$'),
        re.compile(r'^([A-Z\s]{4,40})$'),
    ]

    clause_patterns = [
        re.compile(r'^([0-9]+\.[0-9]+(?:\.[0-9]+)*)\s*(.*)'),
        re.compile(r'^(\([a-zA-Z0-9]+\))\s*(.*)'),
        re.compile(r'^(Clause\s+[0-9]+(?:\.[0-9]+)*)[:\.\-\s]*(.*)', re.IGNORECASE),
    ]

    current_section = "General"
    current_clause = "Preamble"

    for sec in sections:
        page_num = sec.get("page", 1)
        file_name = sec.get("file_name", "document")
        sec_label = sec.get("section", "")
        if sec_label and sec_label != f"Page {page_num}" and sec_label != "General":
            current_section = sec_label

        text_block = sec.get("text", "")
        if not text_block:
            continue

        # Split into distinct paragraphs while preserving structure
        paragraphs = [p.strip() for p in text_block.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [p.strip() for p in text_block.split("\n") if p.strip()]

        for para in paragraphs:
            para_lines = para.split("\n")
            first_line = para_lines[0].strip()

            # Check if this paragraph starts a new Section/Article
            is_section_header = False
            for sp in section_patterns:
                match = sp.match(first_line)
                if match:
                    current_section = first_line
                    current_clause = "Overview"
                    is_section_header = True
                    break

            # Check if this paragraph specifies a numbered subclause
            for cp in clause_patterns:
                cmatch = cp.match(first_line)
                if cmatch:
                    current_clause = cmatch.group(1).strip()
                    break

            # Handle oversized paragraphs/clauses cleanly
            sub_chunks = _split_oversized_text(para, max_chars=max_chars, overlap_chars=overlap_chars)
            for part_idx, sub_text in enumerate(sub_chunks):
                clause_label = current_clause
                if len(sub_chunks) > 1:
                    clause_label = f"{current_clause} (Part {part_idx + 1})"

                chunks.append({
                    "chunk_id": f"doc_chunk_{chunk_counter}",
                    "text": sub_text,
                    "page": page_num,
                    "section": current_section,
                    "clause": clause_label,
                    "source": "uploaded_document",
                    "file_name": file_name
                })
                chunk_counter += 1

    return chunks


def detect_key_clauses_summary(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes extracted chunks and produces attention indicators and key contract metrics.
    Detects critical provisions: Termination, Indemnity, Liability Cap, Governing Law, etc.
    """
    total_words = sum(len(c.get("text", "").split()) for c in chunks)
    estimated_read_time = max(1, round(total_words / 200))

    flags = {
        "Termination Clause": False,
        "Indemnity / Hold Harmless": False,
        "Limitation of Liability": False,
        "Confidentiality / NDA": False,
        "Governing Law & Jurisdiction": False,
        "Dispute Resolution / Arbitration": False,
        "Payment & Invoicing Terms": False,
    }

    matched_details = {}

    for c in chunks:
        content = (c.get("text", "") + " " + c.get("section", "")).lower()

        if not flags["Termination Clause"] and ("terminat" in content or "cancellation" in content):
            flags["Termination Clause"] = True
            matched_details["Termination Clause"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Indemnity / Hold Harmless"] and ("indemnif" in content or "indemnity" in content or "hold harmless" in content):
            flags["Indemnity / Hold Harmless"] = True
            matched_details["Indemnity / Hold Harmless"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Limitation of Liability"] and ("limitation of liability" in content or "liability cap" in content or "aggregate liability" in content):
            flags["Limitation of Liability"] = True
            matched_details["Limitation of Liability"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Confidentiality / NDA"] and ("confidential" in content or "non-disclosure" in content or "trade secret" in content):
            flags["Confidentiality / NDA"] = True
            matched_details["Confidentiality / NDA"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Governing Law & Jurisdiction"] and ("governing law" in content or "jurisdiction" in content or "choice of law" in content):
            flags["Governing Law & Jurisdiction"] = True
            matched_details["Governing Law & Jurisdiction"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Dispute Resolution / Arbitration"] and ("arbitrat" in content or "mediat" in content or "dispute resolution" in content):
            flags["Dispute Resolution / Arbitration"] = True
            matched_details["Dispute Resolution / Arbitration"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

        if not flags["Payment & Invoicing Terms"] and ("payment" in content or "invoice" in content or "fee" in content or "net 30" in content):
            flags["Payment & Invoicing Terms"] = True
            matched_details["Payment & Invoicing Terms"] = f"Page {c.get('page', 1)} • {c.get('clause', 'N/A')}"

    return {
        "total_words": total_words,
        "estimated_read_minutes": estimated_read_time,
        "indicators": flags,
        "matched_citations": matched_details,
        "detected_count": sum(1 for v in flags.values() if v),
        "total_checks": len(flags)
    }


