# -*- coding: utf-8 -*-
"""
LegalDocAiAssist — Professional AI Legal Document Intelligence Platform.

Features:
- Minimalist, executive-grade AI user experience (like ChatGPT / Claude legal workspace)
- Zero technical clutter: Automatic cloud secret / API resolution without exposing keys or models to end-users
- Instant 1-click sample contracts or custom document upload (PDF, DOCX, TXT, MD, Scanned Images)
- Automated Executive Legal Dossier: Plain-language summary, commercial terms, 7-point risk radar, and red flags
- Interactive conversational AI assistant (Chat with Document) with grounded FAISS clause citations
- Authentic bilingual support: English and RTL Urdu (Noto Nastaliq Urdu)
- 100% In-Memory RAM confidentiality & zero data persistence
"""

import os
import io
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LegalDocAiAssist | AI Legal Document Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Executive, High-End AI Legal Product Styling
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #09152b 0%, #0f2b48 50%, #1e3a5f 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
    color: #f8fafc;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(59, 130, 246, 0.22);
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.45);
    padding: 0.3rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-top: 0.6rem;
    font-weight: 400;
    line-height: 1.5;
    max-width: 850px;
}

/* Disclaimer Callout */
.disclaimer-banner {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 0.8rem 1.15rem;
    color: #92400e;
    font-size: 0.85rem;
    line-height: 1.5;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(245, 158, 11, 0.08);
}

/* Cards & Dossier Container */
.executive-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.75rem 2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
    line-height: 1.65;
}

/* Markdown Table Styling for Contracts */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 1.25rem 0 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
}

th {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 0.75rem 1rem !important;
    border-bottom: 2px solid #cbd5e1 !important;
    font-size: 0.88rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
}

td {
    padding: 0.75rem 1rem !important;
    border-bottom: 1px solid #f1f5f9 !important;
    color: #334155 !important;
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
}

tr:nth-child(even) {
    background-color: #f8fafc !important;
}

tr:hover {
    background-color: #f1f5f9 !important;
}

.dossier-content h3 {
    color: #0f172a;
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.35rem;
}

.dossier-content p, .dossier-content li {
    color: #334155;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Active Document Topbar */
.doc-topbar {
    background: linear-gradient(90deg, #f8fafc 0%, #edf2f7 100%);
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 0.85rem 1.25rem;
    margin-bottom: 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.doc-info-badge {
    background: #e2e8f0;
    color: #334155;
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
}

/* Chat bubble styling */
.chat-response-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563eb;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
}

.chat-question-pill {
    background: #eff6ff;
    color: #1e40af;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    display: inline-block;
}

/* Value Props Initial Cards */
.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.35rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
    height: 100%;
}

.feature-card h4 {
    color: #0f172a;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.feature-card p {
    color: #64748b;
    font-size: 0.88rem;
    line-height: 1.5;
    margin: 0;
}

/* RTL Support for Urdu */
.rtl-content {
    direction: rtl;
    text-align: right;
    font-family: 'Noto Nastaliq Urdu', 'Inter', serif;
    line-height: 2.2;
    font-size: 1.05rem;
}

/* Clean buttons */
.stButton>button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.15s ease-in-out;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Import RAG, Gemini client, and Document Processing utilities
from modules.rag import (
    resolve_api_key,
    resolve_model_name,
    retrieve_rag_context,
    generate_grounded_explanation,
    generate_document_dossier,
    DEFAULT_MODEL,
)
from modules.document_processor import (
    process_document,
    chunk_document_sections,
    detect_key_clauses_summary,
)
from modules.embeddings import create_faiss_index

# Root directory paths for sample documents
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "sample_documents")

SAMPLE_DOCUMENTS = {
    "Commercial Master Services Agreement (MSA)": {
        "file": "commercial_services_agreement.pdf",
        "title": "Commercial Master Services Agreement",
        "badge": "B2B Contract • Net 30 Billing • IP & Liability Cap",
        "description": "Comprehensive corporate services contract with Net 30 invoices, intellectual property assignment, indemnification, and liability caps."
    },
    "Mutual Non-Disclosure Agreement (MNDA)": {
        "file": "mutual_non_disclosure_agreement.pdf",
        "title": "Mutual Non-Disclosure Agreement",
        "badge": "Confidentiality • Trade Secrets • Injunctive Relief",
        "description": "Bilateral NDA protecting proprietary data, exclusions from confidentiality, standard of care, and court equitable relief."
    },
    "Residential Tenancy Agreement (Lease)": {
        "file": "residential_tenancy_agreement.pdf",
        "title": "Residential Tenancy Agreement",
        "badge": "Lease Deed • Rent Escalation • Security Deposit",
        "description": "Real estate lease with monthly rent, security deposit terms, 10% annual escalation, tenant covenants, and dispute tribunal venue."
    }
}


def init_session_state():
    """Initialize necessary Streamlit session state variables."""
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "gemini_model" not in st.session_state:
        st.session_state.gemini_model = resolve_model_name()
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = resolve_api_key() or ""
    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False
    if "document_name" not in st.session_state:
        st.session_state.document_name = None
    if "raw_sections" not in st.session_state:
        st.session_state.raw_sections = []
    if "document_chunks" not in st.session_state:
        st.session_state.document_chunks = []
    if "clause_indicators" not in st.session_state:
        st.session_state.clause_indicators = None
    if "doc_index" not in st.session_state:
        st.session_state.doc_index = None
    if "dossier" not in st.session_state:
        st.session_state.dossier = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def reset_app_state():
    """Reset the session state to allow uploading a new document."""
    st.session_state.document_processed = False
    st.session_state.document_name = None
    st.session_state.raw_sections = []
    st.session_state.document_chunks = []
    st.session_state.clause_indicators = None
    st.session_state.doc_index = None
    st.session_state.dossier = None
    st.session_state.chat_history = []
    st.rerun()


def render_sidebar():
    """Render a clean, minimalist sidebar focused solely on language and session status."""
    with st.sidebar:
        st.markdown("### ⚖️ LegalDocAiAssist")
        st.caption("AI-Powered Legal Document Intelligence")

        st.markdown("---")

        # Language Selector
        st.markdown("**🌐 Language / زبان**")
        selected_lang = st.radio(
            label="Language Selection",
            options=["English", "اردو (Urdu)"],
            index=0 if st.session_state.language == "English" else 1,
            label_visibility="collapsed"
        )
        new_lang = "English" if "English" in selected_lang else "Urdu"
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            # Invalidate cached dossier if language changes
            st.session_state.dossier = None
            st.rerun()

        st.markdown("---")

        # Session Status
        if st.session_state.document_processed:
            st.markdown("#### 📑 Active Document")
            st.markdown(f"**`{st.session_state.document_name}`**")
            p_count = len(st.session_state.raw_sections)
            c_count = len(st.session_state.document_chunks)
            st.caption(f"✓ Ingested: **{p_count} Pages** • **{c_count} Clauses**")
            
            if st.button("🔄 Analyze Another File", use_container_width=True, type="secondary"):
                reset_app_state()
        else:
            st.info("No document loaded yet. Upload your agreement or load a demo sample.", icon="💡")

        st.markdown("---")

        # Security & Privacy reassurance
        st.markdown("#### 🔒 Confidentiality Guarantee")
        st.markdown(
            """
            - **100% In-Memory RAM:** Documents and vector embeddings exist only during your active session.
            - **Zero Data Retention:** No documents or confidential clauses are saved to disk or used to train AI models.
            - **Purged on Exit:** Closing or resetting your browser clears all session data instantly.
            """
        )

        st.markdown("---")
        st.caption("LegalDocAiAssist v1.0 • Grounded Legal RAG")


def render_header_and_disclaimer():
    """Render top hero header and educational legal disclaimer."""
    is_urdu = st.session_state.language == "Urdu"

    st.markdown(
        """
        <div class="hero-header">
            <span class="hero-badge">⚡ Autonomous Legal Intelligence • Bilingual</span>
            <h1 class="hero-title">LegalDocAiAssist</h1>
            <p class="hero-subtitle">Upload any legal agreement to instantly generate an executive briefing, evaluate critical contractual risks, and chat with your document in plain English or Urdu.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if is_urdu:
        st.markdown(
            """
            <div class="disclaimer-banner rtl-content">
                ⚖️ <strong>قانونی انتباہ:</strong> LegalDocAiAssist صرف تعلیمی اور معلوماتی مقاصد کے لیے ہے۔ یہ باضابطہ قانونی مشورہ یا وکیل کی نمائندگی فراہم نہیں کرتا۔ کسی بھی معاہدے پر دستخط کرنے سے قبل مستند وکیل سے قانونی رہنمائی حاصل کریں۔
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="disclaimer-banner">
                ⚖️ <strong>Legal Notice:</strong> LegalDocAiAssist provides automated plain-language explanations and risk indicators for educational purposes only. It does not constitute formal legal counsel or attorney representation. Always consult a qualified lawyer before executing contracts.
            </div>
            """,
            unsafe_allow_html=True
        )


def ingest_document(file_bytes: bytes, file_name: str):
    """Core pipeline to process, chunk, index, and generate dossier for a document."""
    with st.spinner("Analyzing document structure, extracting clauses & building AI briefing..."):
        try:
            sections = process_document(
                file_input=file_bytes,
                file_name=file_name,
                gemini_api_key=st.session_state.gemini_api_key,
                gemini_model=st.session_state.gemini_model
            )
            chunks = chunk_document_sections(sections)
            doc_index = create_faiss_index(chunks)
            indicators = detect_key_clauses_summary(chunks)

            # Generate Executive Dossier
            dossier = generate_document_dossier(
                chunks=chunks,
                indicators=indicators,
                language=st.session_state.language,
                api_key=st.session_state.gemini_api_key,
                model_name=st.session_state.gemini_model
            )

            st.session_state.raw_sections = sections
            st.session_state.document_chunks = chunks
            st.session_state.clause_indicators = indicators
            st.session_state.doc_index = doc_index
            st.session_state.document_name = file_name
            st.session_state.dossier = dossier
            st.session_state.document_processed = True
            st.rerun()
        except Exception as err:
            st.error(f"Error processing document: {str(err)}", icon="⚠️")


def render_upload_portal():
    """Render the clean, professional document ingestion portal."""
    st.markdown(
        """
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 1.5rem;">
            <h3 style="color: #0f172a; margin-top: 0; margin-bottom: 0.5rem; font-weight: 700;">📂 Document Ingestion</h3>
            <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem;">
                Select a verified legal sample for an instant walkthrough or upload your own contract:
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_demo, col_upload = st.columns([1, 1], gap="large")

    with col_demo:
        st.markdown("#### ⚡ 1. Try an Authentic Legal Sample")
        st.markdown("Click below to test with a pre-configured legal agreement:")

        chosen_sample_key = st.selectbox(
            "Select sample agreement",
            options=list(SAMPLE_DOCUMENTS.keys()),
            label_visibility="collapsed"
        )
        sample_meta = SAMPLE_DOCUMENTS[chosen_sample_key]
        st.caption(f"ℹ️ **{sample_meta['badge']}**\n\n{sample_meta['description']}")

        if st.button("🚀 Load & Analyze Sample", type="primary", use_container_width=True):
            sample_path = os.path.join(SAMPLE_DOCS_DIR, sample_meta["file"])
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    file_data = f.read()
                ingest_document(file_data, sample_meta["file"])
            else:
                st.error(f"Sample file not found at: {sample_path}")

    with col_upload:
        st.markdown("#### 📤 2. Or Upload Your Legal Document")
        st.markdown("Upload any agreement (PDF, DOCX, TXT, MD, Scanned Images):")

        uploaded_file = st.file_uploader(
            label="Upload Legal Agreement",
            type=["pdf", "docx", "txt", "md", "jpg", "jpeg", "png"],
            help="Supported formats: Digital or Scanned PDF, Word DOCX, TXT, MD, JPG, PNG",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            if hasattr(uploaded_file, "size") and uploaded_file.size == 0:
                st.warning("The uploaded file is empty (0 bytes).")
            else:
                if st.button("🔍 Analyze Uploaded Document", type="primary", use_container_width=True):
                    file_bytes = uploaded_file.read()
                    ingest_document(file_bytes, uploaded_file.name)

    # Clean Value Proposition Highlights
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🔍 Clause-Aware Chunking</h4>
                <p>Preserves structural numbering, section headers, and vital qualifiers like <em>'shall not'</em>, <em>'without penalty'</em>, and <em>'unless'</em>.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class="feature-card">
                <h4>🛡️ Automated Risk Radar</h4>
                <p>Instantly flags key protections: Termination rights, indemnity scope, aggregate liability caps, and dispute resolution venues.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class="feature-card">
                <h4>💬 Grounded Q&A Assistant</h4>
                <p>Chat with your contract using verified dual-source RAG with exact page and clause citations in standard English or authentic Urdu.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_active_document_workspace():
    """Render the clean, executive-level workspace once a document is loaded."""
    is_urdu = st.session_state.language == "Urdu"
    rtl_class = "rtl-content" if is_urdu else ""

    doc_name = st.session_state.document_name or "Contract"
    total_pages = len(st.session_state.raw_sections)
    total_chunks = len(st.session_state.document_chunks)
    indicators = st.session_state.clause_indicators or {}
    total_words = indicators.get("total_words", 0)
    read_mins = indicators.get("estimated_read_minutes", 3)

    # Active Document Status Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(
            f"""
            <div class="doc-topbar">
                <div>
                    <strong style="color: #0f172a; font-size: 1.05rem;">📄 {doc_name}</strong>
                    <div style="margin-top: 0.35rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <span class="doc-info-badge">📑 {total_pages} Ingested Pages</span>
                        <span class="doc-info-badge">⚡ {total_chunks} Legal Clauses Indexed</span>
                        <span class="doc-info-badge">📝 {total_words:,} Words</span>
                        <span class="doc-info-badge">⏱️ ~{read_mins} Min Read Time</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with top_col2:
        if st.button("🔄 Upload / Load New", use_container_width=True, type="secondary"):
            reset_app_state()

    # Generate dossier if not present
    if not st.session_state.dossier:
        with st.spinner("Synthesizing Executive AI Legal Briefing..."):
            st.session_state.dossier = generate_document_dossier(
                chunks=st.session_state.document_chunks,
                indicators=indicators,
                language=st.session_state.language,
                api_key=st.session_state.gemini_api_key,
                model_name=st.session_state.gemini_model
            )

    dossier = st.session_state.dossier or {}
    dossier_text = dossier.get("text", "")

    # -------------------------------------------------------------
    # SECTION 1: PLAIN-ENGLISH CONTRACT BREAKDOWN
    # -------------------------------------------------------------
    card_title = "📋 Plain-English Contract Breakdown" if not is_urdu else "📋 معاہدے کا آسان اردو جائزہ و رہنمائی"
    card_subtitle = "Key terms, tricky clauses & what you must know before signing" if not is_urdu else "بنیادی شرائط، پوشیدہ خطرات اور دستخط سے قبل اہم احتیاطی تدابیر"
    badge_label = "⚡ AI Contract Intelligence" if not is_urdu else "⚡ خودکار قانونی تجزیہ"

    st.markdown(
        f"""
        <div class="executive-card {rtl_class}">
            <div style="border-bottom: 2px solid #e2e8f0; padding-bottom: 0.85rem; margin-bottom: 1rem;">
                <span style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; color: #2563eb; letter-spacing: 0.05em; background: #eff6ff; padding: 0.2rem 0.6rem; border-radius: 9999px;">{badge_label}</span>
                <h2 style="color: #0f172a; font-size: 1.5rem; font-weight: 800; margin: 0.35rem 0 0.2rem 0;">{card_title}</h2>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0;">{card_subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render dossier markdown cleanly inside container
    with st.container():
        st.markdown(f"<div class='dossier-content {rtl_class}'>", unsafe_allow_html=True)
        st.markdown(dossier_text)
        st.markdown("</div>", unsafe_allow_html=True)

    # Download Dossier Button
    st.download_button(
        label="📥 Download Contract Breakdown (.md)",
        data=f"# LegalDocAiAssist Breakdown: {doc_name}\n\n{dossier_text}\n\n---\n*Educational legal AI intelligence report.*",
        file_name=f"{doc_name}_Plain_English_Breakdown.md",
        mime="text/markdown",
        use_container_width=False
    )

    st.markdown("---")

    # -------------------------------------------------------------
    # SECTION 2: CHAT WITH THIS DOCUMENT (INTERACTIVE AI ASSISTANT)
    # -------------------------------------------------------------
    st.markdown("### 💬 Ask Questions About This Document")
    st.caption("Ask anything about this contract. Answers are strictly synthesized from retrieved clauses and verified legal principles:")

    # Quick prompt chips
    st.caption("💡 **Quick Suggested Inquiries:**")
    prompt_col1, prompt_col2, prompt_col3, prompt_col4 = st.columns(4)
    sample_questions = [
        "Can I cancel early and what notice is required?",
        "What are the payment terms and late penalties?",
        "Is there an indemnity trap and who is protected?",
        "What is the biggest hidden risk for me in this contract?"
    ]
    chosen_prompt = None
    with prompt_col1:
        if st.button(sample_questions[0], key="chip_0", use_container_width=True):
            chosen_prompt = sample_questions[0]
    with prompt_col2:
        if st.button(sample_questions[1], key="chip_1", use_container_width=True):
            chosen_prompt = sample_questions[1]
    with prompt_col3:
        if st.button(sample_questions[2], key="chip_2", use_container_width=True):
            chosen_prompt = sample_questions[2]
    with prompt_col4:
        if st.button(sample_questions[3], key="chip_3", use_container_width=True):
            chosen_prompt = sample_questions[3]

    q_col1, q_col2 = st.columns([4, 1.2])
    with q_col1:
        user_query = st.text_input(
            label="Ask a question",
            value=chosen_prompt or "",
            placeholder="e.g. Does this contract have an automatic renewal clause or liability cap?",
            label_visibility="collapsed"
        )
    with q_col2:
        ask_btn = st.button("🚀 Ask Assistant", type="primary", use_container_width=True, disabled=not bool(user_query or chosen_prompt))

    active_query = (user_query or chosen_prompt or "").strip()

    if ask_btn and active_query:
        with st.spinner("Retrieving clauses and synthesizing grounded legal explanation..."):
            rag_payload = retrieve_rag_context(
                query=active_query,
                doc_index=st.session_state.doc_index,
                top_k_doc=4,
                top_k_kb=2
            )

            result = generate_grounded_explanation(
                user_query=active_query,
                rag_payload=rag_payload,
                language=st.session_state.language,
                api_key=st.session_state.gemini_api_key,
                model_name=st.session_state.gemini_model
            )

            st.session_state.chat_history.insert(0, {
                "query": active_query,
                "result": result,
                "payload": rag_payload,
                "language": st.session_state.language
            })

    # Render conversation history
    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        for item in st.session_state.chat_history:
            q = item["query"]
            res = item["result"]
            payload = item["payload"]
            item_urdu = "urdu" in item.get("language", "English").lower()
            item_rtl = "rtl-content" if item_urdu else ""

            st.markdown(f"<div class='chat-question-pill'>❓ {q}</div>", unsafe_allow_html=True)
            
            st.markdown(
                f"""
                <div class="chat-response-card {item_rtl}">
                    <div style="white-space: pre-wrap; font-size: 0.96rem; color: #1e293b; line-height: 1.7;">
{res.get('text', '')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Citations accordion
            doc_chunks = payload.get("doc_chunks", [])
            with st.expander(f"📌 View Retrieved Evidence ({len(doc_chunks)} Clauses)", expanded=False):
                if doc_chunks:
                    for idx, dc in enumerate(doc_chunks):
                        st.markdown(
                            f"- **Citation {idx + 1}:** Page `{dc.get('page', 1)}` • Section `{dc.get('section', 'General')}` • Clause `{dc.get('clause', 'N/A')}`"
                        )
                        st.caption(f"Excerpt: \"{dc.get('text', '')[:200]}...\"")
                else:
                    st.caption("No direct clause matches.")



def main():
    init_session_state()
    render_sidebar()
    render_header_and_disclaimer()

    if not st.session_state.document_processed:
        render_upload_portal()
    else:
        render_active_document_workspace()


if __name__ == "__main__":
    main()
