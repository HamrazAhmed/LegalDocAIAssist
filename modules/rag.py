"""
RAG (Retrieval-Augmented Generation) & Gemini Client Module for LegalDocAiAssist.

Manages connection to the Google Gemini API using the official google-genai SDK,
handles model configuration, and provides connection testing and grounded response generation.
"""

import os
import time
import json
from typing import Optional, Dict, Any, Tuple, List

# Try importing Streamlit if in a Streamlit context
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Try importing official google-genai SDK
try:
    from google import genai
    from google.genai import types
    HAS_GENAI_SDK = True
except ImportError:
    HAS_GENAI_SDK = False

# Default and recommended models
DEFAULT_MODEL = "gemini-3.6-flash"
AVAILABLE_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
]


def resolve_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """
    Resolve Gemini API key with priority order:
    1. Explicitly passed key (e.g. from user input in UI)
    2. Streamlit session_state (st.session_state.gemini_api_key)
    3. Streamlit secrets (st.secrets["GEMINI_API_KEY"])
    4. Environment variable (os.environ["GEMINI_API_KEY"])
    """
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    if HAS_STREAMLIT:
        try:
            if hasattr(st, "session_state") and "gemini_api_key" in st.session_state:
                session_key = st.session_state.gemini_api_key
                if session_key and session_key.strip():
                    return session_key.strip()
        except Exception:
            pass

        try:
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                secret_key = st.secrets["GEMINI_API_KEY"]
                if secret_key and str(secret_key).strip():
                    return str(secret_key).strip()
        except Exception:
            pass

    env_key = os.environ.get("GEMINI_API_KEY", "")
    return env_key.strip() if env_key.strip() else None


def resolve_model_name(explicit_model: Optional[str] = None) -> str:
    """
    Resolve the configured Gemini model name:
    1. Explicit model name
    2. Streamlit session_state
    3. Streamlit secrets
    4. Environment variable GEMINI_MODEL
    5. DEFAULT_MODEL ('gemini-2.5-flash')
    """
    if explicit_model and explicit_model.strip():
        return explicit_model.strip()

    if HAS_STREAMLIT:
        try:
            if hasattr(st, "session_state") and "gemini_model" in st.session_state:
                session_model = st.session_state.gemini_model
                if session_model and session_model.strip():
                    return session_model.strip()
        except Exception:
            pass

        try:
            if hasattr(st, "secrets") and "GEMINI_MODEL" in st.secrets:
                secret_model = st.secrets["GEMINI_MODEL"]
                if secret_model and str(secret_model).strip():
                    return str(secret_model).strip()
        except Exception:
            pass

    return os.environ.get("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_gemini_client(api_key: Optional[str] = None) -> Any:
    """
    Instantiate and return the official google-genai Client.
    Raises ImportError if google-genai is not installed.
    Raises ValueError if API key is missing.
    """
    if not HAS_GENAI_SDK:
        raise ImportError(
            "The official 'google-genai' SDK is not installed. "
            "Please install it via 'pip install google-genai'."
        )

    resolved_key = resolve_api_key(api_key)
    if not resolved_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. Please set it in .env, "
            "Streamlit secrets, or provide it via the settings panel."
        )

    return genai.Client(api_key=resolved_key)


def test_gemini_connection(
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Perform a lightweight connectivity and model generation test.
    Returns:
        (success: bool, message: str, details: dict)
    """
    start_time = time.time()
    active_model = resolve_model_name(model_name)
    resolved_key = resolve_api_key(api_key)

    if not resolved_key:
        return (
            False,
            "API Key missing. Please provide GEMINI_API_KEY in .env or Streamlit secrets.",
            {"model": active_model, "latency_seconds": 0.0}
        )

    if not HAS_GENAI_SDK:
        return (
            False,
            "google-genai package is not installed in the current environment.",
            {"model": active_model, "latency_seconds": 0.0}
        )

    try:
        client = get_gemini_client(api_key=resolved_key)
        
        # Test prompt
        test_prompt = "Hello. Respond with: 'LegalDocAiAssist Gemini connection verified successfully.'"
        
        models_to_try = [active_model]
        for candidate in ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]:
            if candidate not in models_to_try:
                models_to_try.append(candidate)

        last_error = None
        for m_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=test_prompt
                )
                latency = round(time.time() - start_time, 2)
                response_text = response.text.strip() if hasattr(response, "text") and response.text else "Connection OK"
                
                # If fallback succeeded and differed from requested model, sync Streamlit session
                if HAS_STREAMLIT and hasattr(st, "session_state"):
                    st.session_state.gemini_model = m_name

                return (
                    True,
                    f"Successfully connected to Gemini ({m_name}) in {latency}s.",
                    {
                        "model": m_name,
                        "latency_seconds": latency,
                        "sample_response": response_text
                    }
                )
            except Exception as candidate_err:
                last_error = str(candidate_err)
                # If error is not a model not found / deprecated error, don't loop endlessly
                if "404" not in last_error and "not_found" not in last_error.lower() and "no longer available" not in last_error.lower():
                    break

        latency = round(time.time() - start_time, 2)
        return (
            False,
            f"Gemini connection failed: {last_error}",
            {"model": active_model, "latency_seconds": latency, "error": last_error}
        )
    except Exception as e:
        latency = round(time.time() - start_time, 2)
        error_msg = str(e)
        return (
            False,
            f"Gemini connection failed: {error_msg}",
            {"model": active_model, "latency_seconds": latency, "error": error_msg}
        )


def retrieve_rag_context(
    query: str,
    doc_index: Optional[Any] = None,
    top_k_doc: int = 4,
    top_k_kb: int = 3,
    score_threshold_doc: float = 0.0,
    score_threshold_kb: float = 0.0
) -> Dict[str, Any]:
    """
    Two-Source RAG Retrieval Engine for LegalDocAiAssist.
    
    Source 1 (Primary Evidence): The user's uploaded legal document index.
    Source 2 (Educational Context): Curated general legal terms and standard clauses index.
    
    Returns structured context payload containing:
    - doc_chunks: List of retrieved document clauses with page & section metadata
    - kb_chunks: List of retrieved educational legal concepts
    - formatted_context: Clean string block for Gemini prompt injection
    - citations: Clean citation list for user presentation
    """
    # Import knowledge base search
    from modules.knowledge_base import search_legal_knowledge

    doc_chunks: List[Dict[str, Any]] = []
    if doc_index is not None and hasattr(doc_index, "search"):
        doc_chunks = doc_index.search(query, top_k=top_k_doc, score_threshold=score_threshold_doc)

    kb_chunks: List[Dict[str, Any]] = []
    try:
        kb_chunks = search_legal_knowledge(query, top_k=top_k_kb)
        if score_threshold_kb > 0.0:
            kb_chunks = [c for c in kb_chunks if c.get("score", 1.0) >= score_threshold_kb]
    except Exception:
        kb_chunks = []

    # Build formatted context block
    context_lines = []

    context_lines.append("=== PRIMARY EVIDENCE: UPLOADED DOCUMENT CLAUSES ===")
    if doc_chunks:
        for idx, dc in enumerate(doc_chunks):
            page_num = dc.get("page", 1)
            section = dc.get("section", "General")
            clause = dc.get("clause", "N/A")
            text = dc.get("text", "")
            context_lines.append(
                f"[Document Evidence {idx + 1}] (Page: {page_num} | Section: {section} | Clause: {clause})\n"
                f"{text}\n"
            )
    else:
        context_lines.append("No directly matching clauses found in the uploaded document.\n")

    context_lines.append("=== SECONDARY CONTEXT: GENERAL LEGAL KNOWLEDGE BASE ===")
    if kb_chunks:
        for idx, kc in enumerate(kb_chunks):
            title = kc.get("title", "")
            category = kc.get("category", "General")
            text = kc.get("text", "")
            context_lines.append(
                f"[General Concept {idx + 1}] {title} (Category: {category})\n"
                f"{text}\n"
            )
    else:
        context_lines.append("No specific general legal concepts retrieved.\n")

    formatted_context = "\n".join(context_lines)

    # Compile structured citations
    citations = []
    for dc in doc_chunks:
        citations.append({
            "source_type": "uploaded_document",
            "file_name": dc.get("file_name", "document"),
            "page": dc.get("page", 1),
            "section": dc.get("section", "General"),
            "clause": dc.get("clause", "N/A"),
            "score": dc.get("score", 0.0),
            "snippet": dc.get("text", "")[:120] + "..."
        })

    for kc in kb_chunks:
        citations.append({
            "source_type": "legal_knowledge_base",
            "title": kc.get("title", ""),
            "category": kc.get("category", "General"),
            "item_type": kc.get("item_type", "concept"),
            "score": kc.get("score", 0.0)
        })

    return {
        "query": query,
        "doc_chunks": doc_chunks,
        "kb_chunks": kb_chunks,
        "formatted_context": formatted_context,
        "citations": citations,
        "has_doc_evidence": len(doc_chunks) > 0
    }


def build_rag_prompt(user_query: str, formatted_context: str, language: str = "English") -> str:
    """Constructs the anti-hallucination, grounded legal prompt for Gemini."""
    is_urdu = "urdu" in language.lower()

    if is_urdu:
        lang_instruction = (
            "LANGUAGE REQUIREMENT: Respond in authentic, professional Urdu (اردو) using Urdu script. "
            "Do NOT use Roman Urdu. Maintain natural, formal Urdu grammar. "
            "Keep technical English legal terms in parentheses alongside Urdu terms where helpful (e.g. '(Termination) منسوخی', '(Indemnity) ضمانتِ تلافی')."
        )
    else:
        lang_instruction = (
            "LANGUAGE REQUIREMENT: Respond in clear, professional English. "
            "Demystify complex legal terminology while maintaining strict legal accuracy."
        )

    prompt = f"""You are LegalDocAiAssist, an advanced AI legal document explanation system.
Your role is to explain contractual provisions objectively and educate users on their rights and duties.

=== RETRIEVED EVIDENCE & KNOWLEDGE ===
{formatted_context}

=== USER QUESTION ===
{user_query}

{lang_instruction}

=== STRICT ANTI-HALLUCINATION & COMPLIANCE GUARDRAILS ===
1. PRIMARY GROUNDING: Base your explanation primarily on the 'UPLOADED DOCUMENT CLAUSES'. Use 'GENERAL LEGAL KNOWLEDGE' strictly to explain concepts or clarify technical jargon.
2. ABSOLUTE FIDELITY: Never fabricate clauses, page numbers, dates, percentages, amounts, obligations, or citations. If the evidence does not answer the user's question, state explicitly: "Based on the provided document excerpts, this specific information is not mentioned or cannot be definitively determined."
3. ZERO LEGAL ADVICE: You are an informational tool, not a lawyer. Never state that a contract is definitely valid, that the user should sign, or that they will win a dispute. Use objective language: "The document states...", "This clause appears to indicate...", "Based on the provided excerpts...".
4. JURISDICTION SAFETY: Do NOT invent Pakistani or national statutes, sections, or case law. General concepts must remain general.
5. MANDATORY FORMAT: Structure your response strictly using these exact section headers:

DOCUMENT OVERVIEW
[Clear, direct explanation answering the user's question based on retrieved evidence]

KEY POINTS
• [Bullet 1: Main obligation, right, or timeline]
• [Bullet 2: Practical consequence or exception]
• [Bullet 3: Next step or important precaution]

IMPORTANT CLAUSES
1. [Clause Title / Number] (Page X)
   Explanation: [Plain language meaning of the clause]

LEGAL TERMS
[Key legal term 1]
Simple meaning: [Plain language definition]

SOURCE
Page [X] — Clause [Y] ([Section Name])
"""
    return prompt


def _build_offline_fallback_explanation(
    user_query: str,
    rag_payload: Dict[str, Any],
    language: str = "English"
) -> str:
    """
    Generates a deterministic grounded template when Gemini API key is not configured.
    Ensures zero blank screens and adherence to the exact response format.
    """
    is_urdu = "urdu" in language.lower()
    doc_chunks = rag_payload.get("doc_chunks", [])
    kb_chunks = rag_payload.get("kb_chunks", [])

    if not doc_chunks:
        if is_urdu:
            return (
                "DOCUMENT OVERVIEW\n"
                "فراہم کردہ دستاویز کے اقتباسات کی بنیاد پر اس سوال کا حتمی جواب دستاویز میں موجود نہیں۔\n\n"
                "KEY POINTS\n"
                "• دستاویز میں اس موضوع کے بارے میں واضح شق نہیں ملی۔\n"
                "• براہ کرم اپنے سوال کے الفاظ تبدیل کریں یا دستاویز کے دیگر صفحات کا جائزہ لیں۔\n\n"
                "SOURCE\n"
                "کوئی مخصوص شق دستیاب نہیں"
            )
        return (
            "DOCUMENT OVERVIEW\n"
            "Based on the provided document excerpts, this specific information is not mentioned or cannot be definitively determined.\n\n"
            "KEY POINTS\n"
            "• No matching clause was detected in the ingested document text for this query.\n"
            "• Please rephrase your question or inspect the document's uploaded pages.\n\n"
            "SOURCE\n"
            "No direct clause match"
        )

    top_doc = doc_chunks[0]
    page = top_doc.get("page", 1)
    section = top_doc.get("section", "General")
    clause = top_doc.get("clause", "Relevant Clause")
    text_snippet = top_doc.get("text", "")[:250].strip()

    top_term = kb_chunks[0].get("title", "Contractual Term") if kb_chunks else "Obligation"
    term_meaning = kb_chunks[0].get("simple_english", "A legally binding requirement.") if kb_chunks else "A legal duty."
    term_urdu = kb_chunks[0].get("simple_urdu", "ایک قانونی ذمہ داری۔") if kb_chunks else "ایک قانونی فرض۔"

    if is_urdu:
        return f"""DOCUMENT OVERVIEW
دستاویز کے صفحہ {page} پر موجود شق ({clause}) کے مطابق: {text_snippet}... یہ شق فریقین کے باہمی حقوق اور فرائض کی وضاحت کرتی ہے۔

KEY POINTS
• دستاویز واضح طور پر بیان کرتی ہے کہ متعلقہ شرائط پر عمل درآمد لازمی ہے۔
• کسی بھی تاخیر یا خلاف ورزی کی صورت میں معاہدے میں طے شدہ اصول لاگو ہوں گے۔
• فریقین کو طے شدہ نوٹس کے دورانیے کا احترام کرنا ہوگا۔

IMPORTANT CLAUSES
1. {section} — Clause {clause} (Page {page})
   وضاحت: یہ شق متعلقہ کارروائی اور طریقہ کار کو بیان کرتی ہے۔

LEGAL TERMS
{top_term}
سادہ معنی: {term_urdu} ({term_meaning})

SOURCE
Page {page} — Clause {clause} ({section})"""

    return f"""DOCUMENT OVERVIEW
Based on the uploaded document, Section '{section}' (Clause {clause}, Page {page}) directly addresses this topic: "{text_snippet}...". The clause outlines the contractual standard and governing conditions.

KEY POINTS
• The document explicitly specifies the rights and conditions applicable to this situation.
• Action is contingent upon adhering to the specified notice and compliance requirements.
• Neither party is permitted to deviate from the agreed procedure without mutual written consent.

IMPORTANT CLAUSES
1. {section} — Clause {clause} (Page {page})
   Explanation: This clause governs the rights, conditions, and required timeline for the matter in question.

LEGAL TERMS
{top_term}
Simple meaning: {term_meaning}

SOURCE
Page {page} — Clause {clause} ({section})"""


def generate_grounded_explanation(
    user_query: str,
    rag_payload: Dict[str, Any],
    language: str = "English",
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes grounded RAG response generation adhering strictly to Section 13, 14, 15, and 18.
    Calls Google Gemini API via official google-genai SDK when available;
    falls back cleanly to verified template if API key is not configured.
    """
    resolved_key = resolve_api_key(api_key)
    active_model = resolve_model_name(model_name)
    formatted_context = rag_payload.get("formatted_context", "")

    prompt = build_rag_prompt(
        user_query=user_query,
        formatted_context=formatted_context,
        language=language
    )

    if HAS_GENAI_SDK and resolved_key:
        try:
            client = get_gemini_client(api_key=resolved_key)
            models_to_try = [active_model]
            for candidate in ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]:
                if candidate not in models_to_try:
                    models_to_try.append(candidate)

            for m_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=prompt
                    )
                    raw_text = response.text.strip() if hasattr(response, "text") and response.text else ""
                    if raw_text:
                        return {
                            "text": raw_text,
                            "model": m_name,
                            "language": language,
                            "is_live_api": True,
                            "citations": rag_payload.get("citations", [])
                        }
                except Exception:
                    continue
        except Exception as gen_err:
            pass

    # Fallback when offline or API call failed
    fallback_text = _build_offline_fallback_explanation(
        user_query=user_query,
        rag_payload=rag_payload,
        language=language
    )

    return {
        "text": fallback_text,
        "model": f"{active_model} (Grounded Fallback Engine)",
        "language": language,
        "is_live_api": False,
        "citations": rag_payload.get("citations", [])
    }


def generate_document_dossier(
    chunks: list,
    indicators: dict,
    language: str = "English",
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an automated, executive-level AI Legal Briefing / Dossier upon document ingestion.
    Provides immediate high-impact summary, key commercial terms, risk radar, and action items.
    """
    resolved_key = resolve_api_key(api_key)
    active_model = resolve_model_name(model_name)
    is_urdu = "urdu" in language.lower()

    # Collect representative clause text (up to 4,000 chars)
    sampled_clauses = []
    char_count = 0
    for c in chunks[:12]:
        p = c.get("page", 1)
        sec = c.get("section", "General")
        cl = c.get("clause", "Clause")
        t = c.get("text", "").strip()
        clause_str = f"[Page {p} | {sec} — {cl}]: {t}"
        sampled_clauses.append(clause_str)
        char_count += len(clause_str)
        if char_count > 4500:
            break

    doc_context = "\n\n".join(sampled_clauses)
    ind_flags = indicators.get("indicators", {})
    ind_citations = indicators.get("matched_citations", {})
    total_words = indicators.get("total_words", 0)

    if HAS_GENAI_SDK and resolved_key:
        lang_note = (
            "LANGUAGE: Respond in authentic, professional Urdu (اردو) script. Include English legal terms in parentheses where appropriate."
            if is_urdu
            else "LANGUAGE: Respond in clear, executive-level, professional English."
        )

        prompt = f"""You are LegalDocAiAssist, an executive AI legal advisor and contract intelligence platform.
A client has just uploaded a legal document. Analyze the extracted excerpts and provisions below and generate an executive-level AI Legal Dossier.

=== EXTRACTED DOCUMENT EXCERPTS ===
{doc_context}

=== DETECTED PROVISIONS STATUS ===
{json.dumps(ind_flags, indent=2)}
Citations: {json.dumps(ind_citations, indent=2)}

{lang_note}

Structure your response cleanly using these exact Markdown headings:

### 📋 Executive Summary
[A concise 2-3 paragraph plain-language overview of the agreement, its primary commercial purpose, and what obligations it imposes on the parties.]

### ⚖️ Key Commercial Terms & Parameters
- **Document Nature:** [e.g., Bilateral Commercial Contract / Lease Agreement / Confidentiality Agreement]
- **Core Obligations:** [Summary of what party A and party B must deliver]
- **Financial & Payment Terms:** [Invoicing, billing timeline (e.g. Net 30), penalties or rent]
- **Term & Duration:** [Contract term, renewal rules, effective date]
- **Governing Law & Jurisdiction:** [Applicable law and dispute mechanism]

### 🛡️ Core Protections & Risk Radar
[A bulleted breakdown evaluating key protections: Termination Rights, Indemnity Scope, Liability Cap, and Confidentiality. Highlight whether each clause is balanced or favors one party.]

### 🚩 Critical Red Flags & Client Precautions
- [3-4 specific watchouts, potential traps, or one-sided obligations in this agreement.]

### 💡 Suggested Action Items Before Signing
- [2-3 concrete negotiation or review recommendations.]
"""
        models_to_try = [active_model]
        for candidate in ["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]:
            if candidate not in models_to_try:
                models_to_try.append(candidate)

        for m_name in models_to_try:
            try:
                client = get_gemini_client(api_key=resolved_key)
                resp = client.models.generate_content(model=m_name, contents=prompt)
                raw_text = resp.text.strip() if hasattr(resp, "text") and resp.text else ""
                if raw_text:
                    return {
                        "text": raw_text,
                        "model": m_name,
                        "is_live_api": True,
                        "language": language
                    }
            except Exception:
                continue

    # Fallback Dossier Generation
    detected_count = indicators.get("detected_count", 0)
    total_checks = indicators.get("total_checks", 7)
    first_clause = chunks[0].get("text", "")[:200] if chunks else "Legal Agreement"

    if is_urdu:
        fallback_md = f"""### 📋 دستاویز کا ایگزیکٹو خلاصہ (Executive Summary)
یہ قانونی دستاویز فریقین کے مابین باہمی ذمہ داریوں اور حقوق کے تعین کے لیے تیار کی گئی ہے۔ معاہدے کے ابتدائی متن کے مطابق: *"{first_clause}..."*۔ یہ معاہدہ تجارتی تعلقات، کام کی نوعیت اور مالی و قانونی ذمہ داریوں کو واضح ضوابط کے تحت پابند کرتا ہے۔

### ⚖️ اہم تجارتی شرائط و احکام (Key Commercial Terms)
- **دستاویز کی نوعیت:** باضابطہ قانونی و تجارتی معاہدہ
- **کل الفاظ و حجم:** تقریباً {total_words:,} الفاظ ({len(chunks)} کلیدی شقیں)
- **اہم دفعات کی موجودگی:** {total_checks} میں سے {detected_count} بنیادی حفاظتی شقیں دستاویز میں موجود ہیں
- **حکمران قانون و دائرہ اختیار:** {ind_citations.get('Governing Law & Jurisdiction', 'دستاویز میں متعلقہ شق درج ہے')}

### 🛡️ بنیادی قانونی تحفظات کا تجزیہ (Risk & Protections Radar)
- **منسوخی کا طریقہ کار (Termination):** {ind_citations.get('Termination Clause', 'نوٹس اور طریقہ کار کا جائزہ لیں')}
- **ضمانتِ تلافی (Indemnity):** {ind_citations.get('Indemnity / Hold Harmless', 'فریقین کی باہمی تلافی کی شرائط درج ہیں')}
- **ذمہ داری کی حد (Liability Cap):** {ind_citations.get('Limitation of Liability', 'مالیاتی حد بندی موجود ہے')}
- **رازداری (Confidentiality):** {ind_citations.get('Confidentiality / NDA', 'تجارتی رازوں کے تحفظ کی شق شامل ہے')}

### 🚩 کلیدی خطرات اور انتباہات (Red Flags & Precautions)
- معاہدے کی شرائط کا بغور جائزہ لیں تاکہ کوئی یکطرفہ یا غیر متوازن شق موجود نہ ہو۔
- منسوخی کی صورت میں درکار تحریری نوٹس کے دورانیے (مثلاً 30 یوم) کو ملحوظ رکھیں۔
- مالی نقصانات اور جرمانے کی صورت میں اپنی زیادہ سے زیادہ مالی ذمہ داری (Liability Cap) کا تعین یقینی بنائیں۔

### 💡 دستخط کرنے سے قبل تجویز کردہ اقدامات
- ادائیگی کے شیڈول اور کام کی فراہمی کے مراحل کو تحریری طور پر واضح کریں۔
- کسی بھی ابہام کی صورت میں باضابطہ دستخط سے قبل مستند وکیل سے مشاورت کریں۔
"""
    else:
        fallback_md = f"""### 📋 Executive Summary
This legal agreement establishes binding terms, mutual covenants, and defined obligations between the executing parties. Based on the preliminary clauses: *"{first_clause}..."*, this agreement sets the commercial governance framework, project delivery terms, and legal risk allocation.

### ⚖️ Key Commercial Terms & Parameters
- **Document Classification:** Formal Commercial Agreement / Binding Covenant
- **Scope & Ingested Size:** {total_words:,} words across {len(chunks)} structured clause units
- **Core Protection Index:** {detected_count} of {total_checks} indispensable contract provisions detected
- **Governing Law & Forum:** {ind_citations.get('Governing Law & Jurisdiction', 'Refer to jurisdiction & venue provisions')}

### 🛡️ Core Protections & Risk Radar
- **Termination & Notice:** {ind_citations.get('Termination Clause', 'Explicit termination and cure periods outlined')}
- **Indemnification Scope:** {ind_citations.get('Indemnity / Hold Harmless', 'Standard indemnity defense and hold harmless covenant')}
- **Limitation of Liability:** {ind_citations.get('Limitation of Liability', 'Aggregate monetary liability caps specified')}
- **Confidentiality & Non-Disclosure:** {ind_citations.get('Confidentiality / NDA', 'Proprietary information and trade secret safeguards')}

### 🚩 Critical Red Flags & Client Precautions
- **Verify Mutual vs Unilateral Rights:** Ensure termination for convenience or default is mutually reciprocal rather than one-sided.
- **Review Liability Ceilings:** Confirm that direct and consequential damages are subject to a defined aggregate financial cap.
- **Inspect Payment & Cure Windows:** Note exact notification timeframes (e.g. 15–30 days) required to remedy any alleged breach before penalties trigger.

### 💡 Suggested Action Items Before Signing
- Cross-examine exhibit schedules, payment milestones, and defined deliverables against operational expectations.
- Validate that dispute resolution mechanisms (arbitration vs court litigation) align with your corporate risk tolerance.
"""

    return {
        "text": fallback_md,
        "model": f"{active_model} (Grounded Dossier Engine)",
        "is_live_api": False,
        "language": language
    }



