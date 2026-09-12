# -*- coding: utf-8 -*-
"""
LegalDocAiAssist — AI-Powered Legal Document Explanation Platform.

Features:
- Clause-aware document chunking (PDF, DOCX, TXT, MD, Images via Gemini Multimodal OCR)
- Two-source FAISS retrieval (Uploaded Document + General Legal Knowledge Base)
- Grounded Gemini explanation generation with zero-hallucination guardrails
- Bilingual support: Standard English & Authentic RTL Urdu (Noto Nastaliq Urdu)
- One-click demo legal contract loading (Commercial MSA, Mutual NDA, Tenancy Lease)
- Interactive 6-tab dashboard: Overview, Clause Navigator, Grounded Q&A, Knowledge Base, Government Forms, User Guide
- Strict educational disclaimers & confidentiality controls
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
    page_title="LegalDocAiAssist | Legal Intelligence & Explanation",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for an Executive, High-End AI Legal Product Interface
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header container styling */
.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f2b48 100%);
    padding: 2.2rem 2.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1.25rem;
    box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.25);
    color: #f8fafc;
}

.brand-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.brand-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 400;
    line-height: 1.5;
}

/* Badge styling */
.badge-pill {
    display: inline-block;
    background: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.4);
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
}

.badge-tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Legal Disclaimer Callout */
.disclaimer-banner {
    background: linear-gradient(90deg, #fffbeb 0%, #fef3c7 100%);
    border-left: 5px solid #f59e0b;
    border-right: 1px solid #fde68a;
    border-top: 1px solid #fde68a;
    border-bottom: 1px solid #fde68a;
    color: #92400e;
    padding: 0.9rem 1.25rem;
    border-radius: 10px;
    font-size: 0.88rem;
    line-height: 1.5;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 5px rgba(245, 158, 11, 0.08);
}

/* Card components */
.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.35rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

.metric-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
    margin-top: 0.25rem;
}

/* RTL Support for Urdu */
.rtl-content {
    direction: rtl;
    text-align: right;
    font-family: 'Noto Nastaliq Urdu', 'Inter', serif;
    line-height: 2.2;
    font-size: 1.08rem;
}

/* Sample selector container */
.demo-box {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-top: 0.75rem;
    margin-bottom: 1rem;
}

/* Streamlit button enhancement */
.stButton>button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}

/* Sub-card styling */
.clause-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.94rem;
    line-height: 1.6;
    color: #1e293b;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Import RAG, Gemini client, and Document Processing utilities
from modules.rag import (
    resolve_api_key,
    resolve_model_name,
    test_gemini_connection,
    retrieve_rag_context,
    generate_grounded_explanation,
    DEFAULT_MODEL,
    AVAILABLE_MODELS,
    HAS_GENAI_SDK,
)
from modules.document_processor import (
    process_document,
    chunk_document_sections,
    detect_key_clauses_summary,
)
from modules.embeddings import create_faiss_index, get_embedding_dimension
from modules.knowledge_base import (
    load_legal_terms,
    load_common_clauses,
    load_government_forms,
)

# Root directory paths for sample documents
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "sample_documents")

SAMPLE_DOCUMENTS = {
    "Commercial Master Services Agreement (3 Pages - MSA)": {
        "file": "commercial_services_agreement.pdf",
        "title": "Master Services Agreement (MSA)",
        "description": "Comprehensive B2B contract with Term, Net 30 Billing, IP Ownership, Indemnity, Liability Cap, and Arbitration."
    },
    "Mutual Non-Disclosure Agreement (2 Pages - NDA)": {
        "file": "mutual_non_disclosure_agreement.pdf",
        "title": "Mutual Non-Disclosure Agreement (MNDA)",
        "description": "Bilateral confidentiality agreement covering trade secrets, exclusions, standard of care, and court injunctive relief."
    },
    "Residential Tenancy Lease Agreement (2 Pages - Kirayanama)": {
        "file": "residential_tenancy_agreement.pdf",
        "title": "Residential Tenancy Agreement (Kirayanama)",
        "description": "Real estate lease with monthly rent, 10% escalation, security deposit, tenant covenants, and Rent Tribunal jurisdiction."
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
    if "api_test_result" not in st.session_state:
        st.session_state.api_test_result = None
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
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def render_sidebar():
    """Render the configuration, metadata, and status sidebar."""
    with st.sidebar:
        st.markdown("### ⚙️ System Settings")
        
        # Language Selector
        st.markdown("**Language / زبان**")
        selected_lang = st.radio(
            label="Select explanation language",
            options=["English", "اردو (Urdu)"],
            index=0 if st.session_state.language == "English" else 1,
            label_visibility="collapsed"
        )
        st.session_state.language = "English" if "English" in selected_lang else "Urdu"

        st.markdown("---")
        
        # Model & API Status
        st.markdown("### 🤖 Intelligence Engine")

        # Model Selector
        model_options = AVAILABLE_MODELS + ["Custom..."]
        current_model = st.session_state.gemini_model
        model_idx = model_options.index(current_model) if current_model in model_options else len(model_options) - 1

        selected_model = st.selectbox(
            "Gemini Model",
            options=model_options,
            index=model_idx,
            help="Select the Gemini model for multimodal extraction and grounded RAG."
        )

        if selected_model == "Custom...":
            custom_model_input = st.text_input("Enter custom model name", value=current_model)
            st.session_state.gemini_model = custom_model_input.strip() or DEFAULT_MODEL
        else:
            st.session_state.gemini_model = selected_model

        # API Key status and input
        resolved_key = resolve_api_key(st.session_state.gemini_api_key)
        
        if resolved_key:
            st.success("API Key Active (Cloud Secrets)", icon="🔒")
            with st.expander("⚙️ Override API Key (Optional)", expanded=False):
                key_input = st.text_input(
                    "Custom Gemini API Key",
                    value=st.session_state.gemini_api_key,
                    type="password",
                    placeholder="AIzaSy...",
                    help="Optional: Override cloud secret with a custom key."
                )
                if key_input != st.session_state.gemini_api_key:
                    st.session_state.gemini_api_key = key_input
                    st.session_state.api_test_result = None
        else:
            st.warning("API Key Not Detected", icon="⚠️")
            key_input = st.text_input(
                "Gemini API Key",
                value=st.session_state.gemini_api_key,
                type="password",
                placeholder="AIzaSy...",
                help="Set in Streamlit secrets or enter directly here."
            )
            if key_input != st.session_state.gemini_api_key:
                st.session_state.gemini_api_key = key_input
                st.session_state.api_test_result = None

        # Interactive Connection Test Button
        if st.button("🧪 Test Gemini API Connection", use_container_width=True):
            with st.spinner("Connecting to Google Gemini API..."):
                success, message, details = test_gemini_connection(
                    api_key=st.session_state.gemini_api_key,
                    model_name=st.session_state.gemini_model
                )
                st.session_state.api_test_result = {
                    "success": success,
                    "message": message,
                    "details": details
                }

        # Render test results if available
        if st.session_state.api_test_result:
            res = st.session_state.api_test_result
            if res["success"]:
                st.success(res["message"], icon="✅")
                latency = res["details"].get("latency_seconds", 0)
                st.caption(f"⚡ Latency: `{latency}s` • Model: `{res['details'].get('model')}`")
            else:
                st.error(res["message"], icon="❌")
                if not HAS_GENAI_SDK:
                    st.caption("ℹ️ Notice: `google-genai` is listed in requirements.txt for cloud deployment.")

        st.markdown("---")

        # Knowledge Base Status
        st.markdown("### 📚 Legal Knowledge Base")
        all_terms = load_legal_terms()
        all_clauses = load_common_clauses()
        all_forms = load_government_forms()
        dim = get_embedding_dimension()
        st.markdown(
            f"""
            - **Scope:** General Contract & Commercial Law
            - **Legal Terms:** `{len(all_terms)}` indexed
            - **Common Clauses:** `{len(all_clauses)}` cataloged
            - **Statutory Forms:** `{len(all_forms)}` templates
            - **Embedding Dimension:** `{dim}-d` (L2 Normalized)
            - **Confidentiality:** `100% In-Memory RAM`
            """
        )

        st.markdown("---")
        st.caption("LegalDocAiAssist v1.0 • Grounded Legal RAG")


def render_disclaimer():
    """Render the mandatory legal safety disclaimer in English and Urdu."""
    is_urdu = st.session_state.language == "Urdu"
    if is_urdu:
        st.markdown(
            """
            <div class="disclaimer-banner rtl-content">
                ⚖️ <strong>اہم قانونی انتباہ:</strong> LegalDocAiAssist صرف تعلیمی اور معلوماتی مقاصد کے لیے ہے۔ یہ باضابطہ قانونی مشورہ یا وکیل کی نمائندگی فراہم نہیں کرتا۔ کسی بھی معاہدے پر دستخط کرنے یا عدالتی چارہ جوئی سے قبل مستند وکیل سے قانونی رہنمائی حاصل کرنا ضروری ہے۔
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="disclaimer-banner">
                ⚖️ <strong>Mandatory Legal Disclaimer:</strong> LegalDocAiAssist provides educational and informational explanations only. It does NOT constitute formal legal advice, representation, or attorney-client relationship. Always consult a qualified advocate or attorney before executing contracts or pursuing legal claims.
            </div>
            """,
            unsafe_allow_html=True
        )


def render_header():
    """Render the hero brand header."""
    st.markdown(
        """
        <div class="main-header">
            <span class="badge-pill">Dual-Source Grounded RAG • Bilingual AI</span>
            <h1 class="brand-title">LegalDocAiAssist</h1>
            <p class="brand-subtitle">Demystify complex legal contracts, deeds, and agreements with clause-aware structural chunking, risk indicators, and verifiable bilingual explanations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_upload_section():
    """Render the document upload and quick sample loader interface."""
    st.markdown("### 📄 Document Analysis Center")
    st.markdown("Upload your own contract or select a real legal sample agreement for instant demonstration:")

    # Quick Demo Sample Selector
    with st.container():
        st.markdown(
            """
            <div class="demo-box">
                <strong style="color: #0f172a;">⚡ Instant Demo: Load a Pre-configured Legal Agreement</strong>
                <p style="color: #64748b; font-size: 0.85rem; margin: 0.25rem 0 0.5rem 0;">
                    Select any authentic contract to evaluate clause detection, FAISS retrieval, and bilingual Q&A without uploading files:
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        sample_col1, sample_col2 = st.columns([3, 1])
        with sample_col1:
            chosen_sample_key = st.selectbox(
                "Select sample agreement",
                options=list(SAMPLE_DOCUMENTS.keys()),
                label_visibility="collapsed"
            )
        with sample_col2:
            load_sample_btn = st.button("🚀 Load Sample", use_container_width=True, type="secondary")

        if load_sample_btn:
            sample_info = SAMPLE_DOCUMENTS[chosen_sample_key]
            sample_file_path = os.path.join(SAMPLE_DOCS_DIR, sample_info["file"])
            
            if os.path.exists(sample_file_path):
                with st.spinner(f"Loading and indexing '{sample_info['title']}' into FAISS..."):
                    try:
                        with open(sample_file_path, "rb") as f:
                            sample_bytes = f.read()

                        sections = process_document(
                            file_input=sample_bytes,
                            file_name=sample_info["file"],
                            gemini_api_key=st.session_state.gemini_api_key,
                            gemini_model=st.session_state.gemini_model
                        )
                        chunks = chunk_document_sections(sections)
                        doc_index = create_faiss_index(chunks)
                        indicators = detect_key_clauses_summary(chunks)

                        st.session_state.raw_sections = sections
                        st.session_state.document_chunks = chunks
                        st.session_state.clause_indicators = indicators
                        st.session_state.doc_index = doc_index
                        st.session_state.document_name = sample_info["file"]
                        st.session_state.document_processed = True
                        st.toast(f"Successfully loaded '{sample_info['title']}' with {len(chunks)} clauses!", icon="✅")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Error loading sample: {str(err)}", icon="⚠️")
            else:
                st.error(f"Sample file not found at: {sample_file_path}", icon="❌")

    st.markdown("<p style='font-size: 0.9rem; font-weight: 600; color: #475569; margin-top: 0.75rem;'>— OR Upload Your Custom File —</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        label="Select a legal document",
        type=["pdf", "docx", "txt", "md", "jpg", "jpeg", "png"],
        help="Supported formats: PDF (digital or scanned), DOCX, TXT, MD, JPG, JPEG, PNG",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1.2, 1, 2])
    with col1:
        analyze_btn = st.button("🔍 Analyze Uploaded File", type="primary", use_container_width=True, disabled=uploaded_file is None)
    with col2:
        clear_btn = st.button("🔄 Reset / Clear", use_container_width=True, disabled=uploaded_file is None and not st.session_state.document_processed)

    if clear_btn:
        st.session_state.document_processed = False
        st.session_state.document_name = None
        st.session_state.raw_sections = []
        st.session_state.document_chunks = []
        st.session_state.clause_indicators = None
        st.session_state.doc_index = None
        st.session_state.chat_history = []
        st.rerun()

    if analyze_btn and uploaded_file is not None:
        if hasattr(uploaded_file, "size") and uploaded_file.size == 0:
            st.error("The selected file is empty (0 bytes). Please provide a valid legal document.", icon="⚠️")
            return uploaded_file

        with st.spinner("Analyzing document structure, extracting clauses & building FAISS index..."):
            try:
                sections = process_document(
                    file_input=uploaded_file,
                    file_name=uploaded_file.name,
                    gemini_api_key=st.session_state.gemini_api_key,
                    gemini_model=st.session_state.gemini_model
                )
                chunks = chunk_document_sections(sections)
                doc_index = create_faiss_index(chunks)
                indicators = detect_key_clauses_summary(chunks)

                st.session_state.raw_sections = sections
                st.session_state.document_chunks = chunks
                st.session_state.clause_indicators = indicators
                st.session_state.doc_index = doc_index
                st.session_state.document_name = uploaded_file.name
                st.session_state.document_processed = True
                st.toast(f"Successfully indexed {len(chunks)} clause chunks into FAISS!", icon="⚡")
                st.rerun()
            except Exception as exc:
                st.error(f"Document processing notice: {str(exc)}", icon="⚠️")
                st.session_state.document_processed = False

    return uploaded_file


def render_results_section():
    """Render the results dashboard tabs (Overview, Clauses, Q&A, KB, Forms, Guide)."""
    is_urdu = st.session_state.language == "Urdu"

    # Navigation tabs (Available even before document upload for educational knowledge!)
    tab_overview, tab_clauses, tab_qa, tab_terms, tab_forms, tab_guide = st.tabs([
        "📊 Executive Overview" if not is_urdu else "📊 خلاصہ اور جائزہ (Overview)",
        "🔍 Clause Explorer" if not is_urdu else "🔍 شقوں کی تفصیل (Clause Explorer)",
        "💬 Ask AI (Q&A)" if not is_urdu else "💬 سوال و جواب (Ask AI)",
        "📚 Legal Knowledge Base" if not is_urdu else "📚 قانونی اصطلاحات (Knowledge Base)",
        "🏛️ Government Forms Guide" if not is_urdu else "🏛️ سرکاری و قانونی فارمز (Gov Forms)",
        "📖 User Guide & Handbook" if not is_urdu else "📖 رہنمائی و قواعد (User Guide)"
    ])

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------
    with tab_overview:
        if not st.session_state.document_processed:
            st.info("👈 Upload a contract above or click '🚀 Load Sample' to view structural breakdown and clause indicators.")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    """
                    <div class="feature-card">
                        <h4>🔍 Clause-Aware Chunking</h4>
                        <p style="color: #64748b; font-size: 0.9rem;">
                            Preserves numbering, headers, and essential legal qualifiers ('shall not', 'unless', 'must', 'without penalty').
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    """
                    <div class="feature-card">
                        <h4>📚 Dual-Source RAG</h4>
                        <p style="color: #64748b; font-size: 0.9rem;">
                            Pairs retrieved document clauses with curated legal knowledge base to explain technical jargon in simple terms.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c3:
                st.markdown(
                    """
                    <div class="feature-card">
                        <h4>🌐 English & اردو (Urdu)</h4>
                        <p style="color: #64748b; font-size: 0.9rem;">
                            Professional explanations in standard English or authentic RTL Urdu script without losing contractual precision.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            raw_sections = st.session_state.raw_sections
            document_chunks = st.session_state.document_chunks
            total_sections = len(raw_sections)
            total_chunks = len(document_chunks)
            indicators = st.session_state.clause_indicators or {}
            total_words = indicators.get("total_words", 0)
            detected_count = indicators.get("detected_count", 0)
            total_checks = indicators.get("total_checks", 7)

            st.markdown(f"#### 📑 Document Health Check: `{st.session_state.document_name}`")

            # Overview metric cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="metric-title">Ingested Pages</div>
                        <div class="metric-value">{total_sections}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m2:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="metric-title">Identified Legal Chunks</div>
                        <div class="metric-value" style="color: #2563eb;">{total_chunks}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m3:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="metric-title">Total Word Count</div>
                        <div class="metric-value">{total_words:,}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with m4:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="metric-title">Key Provisions Found</div>
                        <div class="metric-value" style="color: {'#10b981' if detected_count >= 5 else '#f59e0b'};">{detected_count} / {total_checks}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🛡️ Automated Contract Provisions & Risk Indicators")
            st.caption("Checks for 7 indispensable protections every commercial contract should contain:")

            ind_flags = indicators.get("indicators", {})
            ind_citations = indicators.get("matched_citations", {})

            col_ind1, col_ind2 = st.columns(2)
            for idx, (check_name, is_present) in enumerate(ind_flags.items()):
                target_col = col_ind1 if idx % 2 == 0 else col_ind2
                with target_col:
                    badge_style = "background: rgba(16, 185, 129, 0.12); color: #059669; border: 1px solid rgba(16, 185, 129, 0.35);" if is_present else "background: rgba(245, 158, 11, 0.12); color: #d97706; border: 1px solid rgba(245, 158, 11, 0.35);"
                    badge_label = "✅ FOUND" if is_present else "⚠️ NOT SPECIFIED"
                    citation_info = f"Reference: <strong>{ind_citations.get(check_name, '')}</strong>" if is_present else "No standard explicit provision found in document text."

                    st.markdown(
                        f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 600; font-size: 0.95rem; color: #1e293b;">{check_name}</span>
                                <span style="padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; {badge_style}">{badge_label}</span>
                            </div>
                            <div style="font-size: 0.83rem; color: #64748b; margin-top: 0.35rem;">{citation_info}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("👁️ View Extracted Document Text by Page", expanded=False):
                for idx, sec in enumerate(raw_sections):
                    st.markdown(f"**Section {idx + 1} — {sec.get('section', 'General')} (Page {sec.get('page', 1)})**")
                    st.text_area(
                        label=f"Content {idx + 1}",
                        value=sec.get("text", ""),
                        height=150,
                        disabled=True,
                        key=f"extracted_preview_{idx}"
                    )

    # -------------------------------------------------------------
    # TAB 2: CLAUSE EXPLORER
    # -------------------------------------------------------------
    with tab_clauses:
        if not st.session_state.document_processed:
            st.info("👈 Please load a sample or upload a document to view indexed clauses.")
        else:
            document_chunks = st.session_state.document_chunks
            st.markdown(f"#### 📜 Indexed Contract Clauses ({len(document_chunks)} total)")
            
            clause_filter = st.text_input("🔍 Filter clauses by keyword (e.g. 'Termination', 'Indemnification', 'Payment', 'Liability')", "").strip().lower()

            filtered_chunks = [
                c for c in document_chunks
                if not clause_filter or clause_filter in c["text"].lower() or clause_filter in c["section"].lower() or clause_filter in c["clause"].lower()
            ]

            if not filtered_chunks:
                st.warning("No clauses match your filter criteria.")
            else:
                for idx, chunk in enumerate(filtered_chunks):
                    section_name = chunk.get("section", "General")
                    clause_name = chunk.get("clause", "Clause")
                    page_num = chunk.get("page", 1)
                    
                    header_label = f"📄 Page {page_num} • {section_name} — {clause_name}"
                    with st.expander(header_label, expanded=(idx < 2)):
                        col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
                        with col_m1:
                            st.caption(f"**Page:** `{page_num}`")
                        with col_m2:
                            st.caption(f"**Section:** `{section_name}`")
                        with col_m3:
                            st.caption(f"**Clause:** `{clause_name}`")
                        
                        st.markdown(
                            f"""
                            <div class="clause-box">
                                {chunk.get('text', '')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    # -------------------------------------------------------------
    # TAB 3: GROUNDED AI LEGAL ASSISTANT (Q&A)
    # -------------------------------------------------------------
    with tab_qa:
        st.markdown("#### 💬 Ask Grounded Legal Questions")
        st.caption("Answers are strictly synthesized from retrieved contract evidence and verified legal knowledge.")

        # Quick Suggested Prompts
        st.caption("💡 **Quick Suggested Prompts:**")
        chip_cols = st.columns(4)
        sample_questions = [
            "What are the termination conditions and notice periods?",
            "What are the payment milestones and late penalties?",
            "Is there an indemnity clause and who is protected?",
            "What law governs this contract and how are disputes resolved?"
        ]
        chosen_prompt = None
        for i, sq in enumerate(sample_questions):
            with chip_cols[i]:
                if st.button(sq, key=f"quick_prompt_{i}", use_container_width=True):
                    chosen_prompt = sq

        user_query = st.text_input(
            "Enter your question",
            value=chosen_prompt or "",
            placeholder="e.g., Can the client cancel early for convenience, and what cure period applies to breaches?",
            label_visibility="collapsed"
        )
        col_ask1, col_ask2 = st.columns([1.2, 4])
        with col_ask1:
            ask_btn = st.button("🚀 Ask AI Assistant", type="primary", use_container_width=True, disabled=not bool(user_query or chosen_prompt))

        active_query = (user_query or chosen_prompt or "").strip()

        if ask_btn and active_query:
            if st.session_state.doc_index is None:
                st.warning("⚠️ Please upload a document or load a demo sample contract first.")
            else:
                with st.spinner("Retrieving evidence and synthesizing grounded explanation with Gemini..."):
                    rag_payload = retrieve_rag_context(
                        query=active_query,
                        doc_index=st.session_state.doc_index,
                        top_k_doc=3,
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

        # Display conversation history
        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            # Download report button
            report_lines = [
                f"# LegalDocAiAssist Explanation Report: {st.session_state.document_name or 'Analysis'}\n",
                f"Generated at: Document Session • Language: {st.session_state.language}\n",
                "> Legal Disclaimer: LegalDocAiAssist provides educational and informational explanations only and does not constitute formal legal advice.\n\n"
            ]
            for item in st.session_state.chat_history:
                report_lines.append(f"## Question: {item['query']}\n\n{item['result'].get('text', '')}\n\n---\n")
            
            full_report = "\n".join(report_lines)
            st.download_button(
                label="📥 Download Explanation Report (.md)",
                data=full_report,
                file_name=f"{st.session_state.document_name or 'contract'}_analysis_report.md",
                mime="text/markdown",
                use_container_width=False
            )
            st.markdown("<br>", unsafe_allow_html=True)

            for item_idx, item in enumerate(st.session_state.chat_history):
                q = item["query"]
                res = item["result"]
                payload = item["payload"]
                item_lang = item.get("language", "English")
                is_item_urdu = "urdu" in item_lang.lower()

                st.markdown(f"### ❓ Question: *\"{q}\"*")

                # Grounded Answer Card
                rtl_class = "rtl-content" if is_item_urdu else ""
                st.markdown(
                    f"""
                    <div class="feature-card {rtl_class}" style="border-left: 5px solid #2563eb; margin-bottom: 1rem; white-space: pre-wrap;">
{res.get('text', '')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Source Citations and Model Info
                with st.expander(f"📌 View Retrieved Evidence & Citations ({len(payload.get('doc_chunks', []))} clauses)", expanded=False):
                    doc_chunks = payload.get("doc_chunks", [])
                    kb_chunks = payload.get("kb_chunks", [])

                    if doc_chunks:
                        st.markdown("**📄 Uploaded Document Citations:**")
                        for c_idx, dc in enumerate(doc_chunks):
                            st.markdown(
                                f"- **Citation {c_idx + 1}:** Page `{dc.get('page', 1)}` • Section `{dc.get('section', 'General')}` • Clause `{dc.get('clause', 'N/A')}` "
                                f"*(Similarity Score: `{dc.get('score', 0)}`)*"
                            )
                            st.caption(f"Excerpt: {dc.get('text', '')[:180]}...")

                    if kb_chunks:
                        st.markdown("<br>**📚 General Legal Knowledge Context:**", unsafe_allow_html=True)
                        for kc in kb_chunks:
                            st.markdown(f"- **{kc.get('title', '')}** ({kc.get('category', 'Concept')}): {kc.get('simple_english', '')}")

                    st.caption(f"⚡ Model: `{res.get('model')}` • Engine: `Dual-Source FAISS Grounding`")

                # Mandatory Disclaimer per response
                st.markdown(
                    """
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.25rem; margin-bottom: 1.5rem; font-style: italic;">
                        ⚖️ LegalDocAiAssist provides educational explanations only and does not constitute formal legal counsel.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("---")

    # -------------------------------------------------------------
    # TAB 4: LEGAL KNOWLEDGE BASE & GLOSSARY
    # -------------------------------------------------------------
    with tab_terms:
        st.markdown("#### 📚 Curated Legal Knowledge Base & Glossary")
        st.markdown("Explore real-world legal definitions, plain-English explanations, authentic Urdu translations, and drafting risk flags:")

        view_mode = st.radio(
            "Select knowledge dataset:",
            ["📖 76+ Legal Terms Glossary", "📜 53+ Common Contract Clauses"],
            horizontal=True,
            label_visibility="collapsed"
        )

        kb_search = st.text_input("🔍 Search legal terms or clauses...", placeholder="e.g., Liquidated Damages, Specific Performance, Indemnity, Force Majeure").strip().lower()

        if "Terms" in view_mode:
            all_terms = load_legal_terms()
            filtered_terms = [
                t for t in all_terms
                if not kb_search or kb_search in t["term"].lower() or kb_search in t.get("definition", "").lower() or kb_search in t.get("simple_english", "").lower()
            ]

            st.caption(f"Showing **{len(filtered_terms)}** of **{len(all_terms)}** authentic legal terms")
            for t in filtered_terms:
                with st.expander(f"🔹 {t['term']} — {t.get('category', 'General Principle')}", expanded=False):
                    st.markdown(f"**Formal Legal Definition:** {t.get('definition', '')}")
                    st.markdown(f"**Plain English:** {t.get('simple_english', '')}")
                    
                    if t.get("simple_urdu"):
                        st.markdown(
                            f"""
                            <div class="rtl-content" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
                                <strong>اردو میں وضاحت:</strong> {t.get('simple_urdu')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    if t.get("important_note"):
                        st.info(f"💡 **Key Legal Insight:** {t.get('important_note')}")
                    if t.get("aliases"):
                        st.caption(f"🏷️ **Related Synonyms:** {', '.join(t.get('aliases', []))}")
        else:
            all_clauses = load_common_clauses()
            filtered_clauses = [
                c for c in all_clauses
                if not kb_search or kb_search in c["clause"].lower() or kb_search in c.get("meaning", "").lower() or kb_search in c.get("simple_english", "").lower()
            ]

            st.caption(f"Showing **{len(filtered_clauses)}** of **{len(all_clauses)}** standard contractual provisions")
            for c in filtered_clauses:
                with st.expander(f"📜 {c['clause']} — {c.get('category', 'Contractual Provision')}", expanded=False):
                    st.markdown(f"**Legal Meaning:** {c.get('meaning', '')}")
                    st.markdown(f"**Plain English:** {c.get('simple_english', '')}")
                    
                    if c.get("simple_urdu"):
                        st.markdown(
                            f"""
                            <div class="rtl-content" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem; margin: 0.5rem 0;">
                                <strong>اردو میں وضاحت:</strong> {c.get('simple_urdu')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    if c.get("what_to_look_for"):
                        st.warning(f"⚠️ **Risks & Red Flags to Check:** {c.get('what_to_look_for')}")

    # -------------------------------------------------------------
    # TAB 5: GOVERNMENT & STATUTORY FORMS GUIDE
    # -------------------------------------------------------------
    with tab_forms:
        st.markdown("#### 🏛️ Government, Statutory & Legal Forms Guide")
        st.markdown("Practical reference guidelines for 8 common legal deeds, statutory returns, and contractual instruments:")

        all_forms = load_government_forms()
        for f_idx, form in enumerate(all_forms):
            with st.expander(f"📑 {form.get('form_type', 'Legal Form')}", expanded=(f_idx == 0)):
                st.markdown(f"**Legal Purpose:** {form.get('purpose', '')}")
                
                st.markdown("##### 📋 Essential Fields & Requirements:")
                fields = form.get("common_fields", [])
                for fld in fields:
                    st.markdown(f"- **{fld.get('field_name')}:** {fld.get('description')}")
                    if fld.get("simple_urdu"):
                        st.caption(f"*(اردو: {fld.get('simple_urdu')})*")

                st.markdown("##### 📎 Typical Supporting Documents & Prerequisites:")
                docs = form.get("typical_supporting_docs", [])
                for doc_item in docs:
                    st.markdown(f"  • {doc_item}")

                if form.get("important_notes"):
                    st.error(f"⚠️ **Critical Legal / Registration Notice:** {form.get('important_notes')}")

    # -------------------------------------------------------------
    # TAB 6: IN-APP USER GUIDE & BEST PRACTICES
    # -------------------------------------------------------------
    with tab_guide:
        st.markdown("#### 📖 LegalDocAiAssist User Guide & Handbook")
        st.markdown("Master contract analysis, risk evaluation, and AI-grounded verification:")

        c_g1, c_g2 = st.columns(2)
        with c_g1:
            st.markdown(
                """
                <div class="feature-card">
                    <h4>🎯 How to Audit a Contract in 4 Steps</h4>
                    <ol style="color: #475569; font-size: 0.9rem; padding-left: 1.2rem; line-height: 1.8;">
                        <li><strong>Check Executive Overview:</strong> Review the 7 core contract provisions indicator to identify missing protections.</li>
                        <li><strong>Examine Termination & Payment:</strong> Filter clauses to confirm notice periods (e.g. 30 days) and cure mechanisms.</li>
                        <li><strong>Inspect Liabilities & Indemnity:</strong> Check whether indemnity is mutual and if an aggregate liability cap exists.</li>
                        <li><strong>Ask Grounded Questions:</strong> Use the Q&A tab with specific questions to receive citation-backed answers.</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_g2:
            st.markdown(
                """
                <div class="feature-card">
                    <h4>🚩 5 Dangerous Contract Red Flags</h4>
                    <ul style="color: #475569; font-size: 0.9rem; padding-left: 1.2rem; line-height: 1.8;">
                        <li><strong>Unilateral Termination for Convenience:</strong> One party can walk away anytime without cause while you cannot.</li>
                        <li><strong>Uncapped Indemnity:</strong> Agreeing to defend third-party claims without any financial ceiling.</li>
                        <li><strong>No Cure Period for Breach:</strong> Immediate termination upon any alleged default without 14-30 days to fix it.</li>
                        <li><strong>Vague Acceptance Criteria:</strong> Client can withhold payment indefinitely based on subjective satisfaction.</li>
                        <li><strong>Inconvenient Foreign Jurisdiction:</strong> Disputes forced into expensive foreign courts with unfamiliar procedures.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="feature-card">
                <h4>🔒 Privacy & Zero-Retention Security Policy</h4>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.7;">
                    LegalDocAiAssist is engineered with strict confidentiality controls:
                </p>
                <ul style="color: #475569; font-size: 0.9rem; padding-left: 1.2rem; line-height: 1.7;">
                    <li><strong>100% In-Memory Processing:</strong> Uploaded documents and FAISS vector embeddings reside only in volatile session RAM and are purged upon clicking 'Reset / Clear' or closing the browser.</li>
                    <li><strong>No Local File Leaks:</strong> Uploaded contracts and confidential vector caches are strictly gitignored and never committed to version control.</li>
                    <li><strong>Zero Model Training:</strong> Document text is transmitted via enterprise API solely for grounded prompt synthesis without fine-tuning public AI models.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )


def main():
    init_session_state()
    render_sidebar()
    render_disclaimer()
    render_header()
    render_upload_section()
    render_results_section()


if __name__ == "__main__":
    main()
