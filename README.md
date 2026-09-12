# LegalDocAiAssist ⚖️🤖

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-2.5--flash-4285F4.svg)](https://ai.google.dev/)
[![FAISS Vector Search](https://img.shields.io/badge/FAISS-Dense%20Retrieval-green.svg)](https://github.com/facebookresearch/faiss)
[![Test Suite](https://img.shields.io/badge/Tests-15%2F15%20Passing-success.svg)](file:///tests/test_pipeline.py)
[![Bilingual](https://img.shields.io/badge/Language-English%20%7C%20%D8%A7%D8%B1%D8%AF%D9%88%20(Urdu)-orange.svg)](#bilingual-english--urdu-support)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**LegalDocAiAssist** is an enterprise-grade AI legal document explanation platform designed to demystify complex contracts, deeds, and agreements. By combining **clause-aware structural chunking**, **384-dimensional dense semantic embeddings (`all-MiniLM-L6-v2`)**, **dual-source FAISS retrieval**, and **Google Gemini intelligence**, LegalDocAiAssist delivers verifiable, evidence-grounded legal explanations in both **English** and **Urdu (اردو)** with zero hallucination.

---

> [!IMPORTANT]
> **Educational & Informational Purpose Only**:
> LegalDocAiAssist provides educational and informational document explanations only. It does **NOT** constitute formal legal advice, representation, or an attorney-client relationship. For binding legal decisions, contract reviews, or courtroom disputes, always consult a qualified legal advocate or attorney.

---

## 🌟 Key Highlights & Capabilities

- 📄 **Universal Document Ingestion**: Ingests **PDF** (digital and scanned), **DOCX**, **TXT**, **MD**, and images (**PNG, JPG, JPEG**) with automatic Gemini Multimodal OCR fallback.
- ⚡ **1-Click Instant Demo Contracts**: Test the pipeline instantly without searching for files—comes with 3 authentic legal contract templates (`Commercial MSA`, `Mutual NDA`, and `Residential Lease`).
- 🔍 **Clause-Aware Structural Chunking**: Parses documents along natural legal boundaries (Sections, Articles, Clauses) while preserving essential legal qualifiers (`shall not`, `unless`, `must`, `without penalty`).
- 🛡️ **Automated Contract Provision Health Check**: Instantly checks for the presence or absence of **7 indispensable contract provisions** (Termination, Indemnity, Liability Cap, NDA, Governing Law, Arbitration, Payment Terms).
- 📚 **Dual-Source Grounded RAG**:
  1. *Primary Evidence*: Direct clause citations from the uploaded contract with page numbers and similarity scores.
  2. *Secondary Knowledge*: Curated legal knowledge base (**76+ terms**, **53+ clauses**, **8 statutory forms**) defining technical jargon in plain language.
- 🌐 **Native Bilingual Support (English & Authentic RTL Urdu)**: Generates structured legal briefs in standard English or beautiful Right-to-Left (RTL) Urdu rendered with the `Noto Nastaliq Urdu` font.
- 📊 **Executive 6-Tab Streamlit Interface**:
  1. **📊 Executive Overview**: Document metrics, provision detection indicators, and extracted text reader.
  2. **🔍 Clause Explorer**: Live keyword search and category filtering across all indexed clauses.
  3. **💬 Grounded AI Assistant (Q&A)**: Interactive chat with suggested prompts, evidence citations, and Markdown report export.
  4. **📚 Legal Knowledge Base**: Searchable glossary of 76+ legal terms and 53+ standard clauses with English & Urdu translations.
  5. **🏛️ Government Forms Guide**: Comprehensive overview of 8 statutory Pakistani legal deeds with mandatory fields and registration traps.
  6. **📖 In-App User Guide & Handbook**: 4-step contract audit tutorial, 5 dangerous clause red flags, and privacy transparency.
- 🔒 **Zero-Retention Confidentiality**: Uploaded documents and FAISS vector embeddings reside **100% in volatile session RAM** and are permanently wiped upon session reset or browser exit.

---

## 🏗️ Technical Architecture & RAG Pipeline

```
┌────────────────────────────────────────────────────────────────────────┐
│                        USER INPUT & INGESTION                          │
│  Uploaded Document (PDF / DOCX / TXT / MD)  OR  1-Click Demo Contract  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      DOCUMENT PROCESSING ENGINE                        │
│  • Digital PDF Extraction (PyMuPDF / Stream Parsing)                   │
│  • Scanned Pages & Image Fallback (Gemini Multimodal OCR)              │
│  • Qualifier-Preserving Cleaner (Retains 'shall not', 'unless', etc.)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     CLAUSE-AWARE CHUNKING LAYER                        │
│  • Section & Clause Regex Boundary Detection                           │
│  • Metadata Enrichment (chunk_id, page, section, clause, source)       │
│  • 7 Core Contract Provisions Detection (Termination, Indemnity, etc.) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 DENSE EMBEDDINGS (all-MiniLM-L6-v2)                    │
│                 384-Dimensional Vectors • L2 Normalized                │
└─────────────────┬───────────────────────────────────┬──────────────────┘
                  │                                   │
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌──────────────────────────────────┐
│   UPLOADED DOCUMENT FAISS INDEX   │ │   LEGAL KNOWLEDGE BASE FAISS     │
│   (IndexFlatIP - Cosine Similarity│ │   (76+ Terms, 53+ Clauses,       │
│    Ephemeral in Session RAM)      │ │    8 Statutory Legal Forms)      │
└─────────────────┬─────────────────┘ └──────────────────┬───────────────┘
                  │                                      │
                  └──────────────────┬───────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      DUAL-SOURCE CONTEXT FUSION                        │
│     Top-K Document Clauses + Top-K Curated Knowledge Definitions       │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    GROUNDED GEMINI INFERENCE ENGINE                    │
│  • Strict Anti-Hallucination Prompting (Zero Local Law Invention)      │
│  • Multi-Tier Key Resolution (UI Input > Session > Secrets > .env)     │
│  • Model Default: gemini-2.5-flash (Configurable / Extensible)         │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      EXECUTIVE STREAMLIT DASHBOARD                     │
│  • Bilingual Reports (English / RTL Urdu with Noto Nastaliq Urdu)      │
│  • 6 Interactive Dashboard Tabs & Downloadable Markdown Reports        │
│  • Mandatory Educational Disclaimers on Every Generated Card           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
LegalDocAiAssist/
├── app.py                         # Main Streamlit application (6 tabs + Demo loader)
├── requirements.txt               # Cloud deployment dependencies
├── README.md                      # Comprehensive project documentation
├── .gitignore                     # Enterprise-grade exclusion matrix
├── .env.example                   # Environment configuration template (0 secrets)
│
├── modules/                       # Core engine modules
│   ├── __init__.py                # Package initializer
│   ├── document_processor.py      # PDF, DOCX, TXT, MD & Multimodal OCR processor
│   ├── embeddings.py              # MiniLM 384-d dense embeddings & FAISS index manager
│   ├── knowledge_base.py          # Curated legal terms, clauses & forms indexer
│   └── rag.py                     # Dual-source retrieval & grounded Gemini synthesis
│
├── knowledge_base/                # Curated educational datasets
│   ├── legal_terms.json           # 76+ terms with definitions, Urdu, and practical notes
│   ├── common_clauses.json        # 53+ clauses with categories, meanings, and risk flags
│   └── government_forms.json      # 8 statutory deed guidelines & registration rules
│
├── sample_documents/              # Pre-configured legal contracts for instant testing
│   ├── commercial_services_agreement.pdf   # 3-page Master Services Agreement (MSA)
│   ├── commercial_services_agreement.txt
│   ├── mutual_non_disclosure_agreement.pdf # 2-page Bilateral Non-Disclosure Agreement
│   ├── mutual_non_disclosure_agreement.txt
│   ├── residential_tenancy_agreement.pdf   # 2-page Tenancy Lease (Kirayanama)
│   └── residential_tenancy_agreement.txt
│
├── scripts/                       # Maintenance and asset generation utilities
│   ├── expand_knowledge_base.py   # Dataset enrichment script
│   └── generate_sample_legal_docs.py # Sample contract generator
│
└── tests/
    └── test_pipeline.py           # 15 automated end-to-end unit tests
```

---

## 🔒 GitHub Push Safety & Confidentiality Matrix

To ensure absolute confidentiality and zero accidental leaks when publishing this repository to GitHub, all sensitive patterns are strictly suppressed by [`.gitignore`](file:///c:/Projects/Development/LegalDocAIAssist/.gitignore):

| Category | File / Pattern | Status on GitHub | Safeguard Purpose |
| :--- | :--- | :--- | :--- |
| **API Keys & Secrets** | `.env`, `.env.*` | 🚫 **NEVER PUSHED** | Prevents exposure of live `GEMINI_API_KEY` |
| **Streamlit Secrets** | `.streamlit/secrets.toml` | 🚫 **NEVER PUSHED** | Cloud environment credentials stay local |
| **Uploads & Temporary Files**| `uploads/`, `temp/`, `scratch/` | 🚫 **NEVER PUSHED** | Prevents user contracts or OCR crops from leaking |
| **Vector Indexes & Caches** | `*.faiss`, `*.index`, `*.pkl` | 🚫 **NEVER PUSHED** | Embeddings remain 100% ephemeral in RAM |
| **Python Bytecode & Logs** | `__pycache__/`, `*.log`, `.pytest_cache/` | 🚫 **NEVER PUSHED** | Build artifacts and system logs ignored |
| **Safe Configuration** | [`.env.example`](file:///c:/Projects/Development/LegalDocAIAssist/.env.example) | ✅ **SAFE TO PUSH** | Blank template showing required variable names |
| **Application Logic** | [`app.py`](file:///c:/Projects/Development/LegalDocAIAssist/app.py), [`modules/*.py`](file:///c:/Projects/Development/LegalDocAIAssist/modules/) | ✅ **SAFE TO PUSH** | Core open-source application code |
| **Educational Datasets** | [`knowledge_base/*.json`](file:///c:/Projects/Development/LegalDocAIAssist/knowledge_base/) | ✅ **SAFE TO PUSH** | Curated legal terminology and clause templates |
| **Sample Contracts** | [`sample_documents/*`](file:///c:/Projects/Development/LegalDocAIAssist/sample_documents/) | ✅ **SAFE TO PUSH** | Synthetic, realistic legal templates for demo |
| **Automated Tests** | [`tests/test_pipeline.py`](file:///c:/Projects/Development/LegalDocAIAssist/tests/test_pipeline.py) | ✅ **SAFE TO PUSH** | Continuous integration unit tests |

---

## 📚 Educational Legal Knowledge Base

LegalDocAiAssist includes a rich, localized legal knowledge base indexed into a dedicated FAISS vector index:

### 1. Legal Terms Glossary (`knowledge_base/legal_terms.json` - 76 Terms)
Contains definitions, simplified English, authentic Urdu translations, key practical notes, and aliases:
- *Core Foundations:* Contract, Agreement, Consideration, Party, Right, Duty, Obligation, Capacity, Privity of Contract, Bona Fide, Mala Fide.
- *Remedies & Damages:* Liquidated Damages, Specific Performance, Injunction, Rescission, Quantum Meruit, Equitable Relief, Restitution.
- *Risk & Liability:* Indemnification, Limitation of Liability, Joint and Several Liability, Subrogation, Force Majeure, Warranties.
- *Commercial Principles:* Caveat Emptor, Fiduciary Duty, Clean Hands Doctrine, Parol Evidence Rule, De Minimis, Mutatis Mutandis, Sine Qua Non, Pro Rata, Ipso Facto.

### 2. Standard Common Clauses (`knowledge_base/common_clauses.json` - 53 Clauses)
Contains legal meanings, plain explanations, Urdu translations, and drafting risk flags:
- *Essential Provisions:* Scope of Work, Payment Terms, Term & Duration, Termination for Cause, Termination for Convenience.
- *Protective Provisions:* Indemnity, Limitation of Liability, Confidentiality, Intellectual Property Ownership, Insurance, Non-Compete, Non-Solicitation.
- *Governance & Boilerplate:* Governing Law, Dispute Resolution & Arbitration, Audit & Inspection Rights, Non-Disparagement, Cumulative Remedies, Counterparts & Electronic Signatures, Successors & Assigns, Time of the Essence, Anti-Bribery Compliance, Change of Control, Set-Off Rights, Severability.

### 3. Government & Statutory Forms Guide (`knowledge_base/government_forms.json` - 8 Templates)
Comprehensive guidelines covering legal purpose, mandatory fields, supporting documents, and statutory registration requirements:
1. **General / Special Power of Attorney** (*Mukhtar Nama Aam / Khas*)
2. **Affidavit / Statutory Declaration** (*Half-Nama*)
3. **Residential & Commercial Tenancy Agreement** (*Kirayanama*)
4. **SECP Form 29** (*Particulars of Directors, CEO & Corporate Officers*)
5. **Deed of Sale of Immovable Property** (*Sale Deed / Bayanama*)
6. **Partnership Deed** (*Form A / Form B Registration under Partnership Act*)
7. **Employment Contract & Letter of Appointment**
8. **Business Registration & Tax Identification** (*NTN / FBR Enrollment*)

---

## 📄 Pre-Configured Sample Documents

Located in [`sample_documents/`](file:///c:/Projects/Development/LegalDocAIAssist/sample_documents/), these synthetic agreements can be loaded with **1 click** from the app UI:

| Document | Format | Description |
| :--- | :--- | :--- |
| **Commercial Master Services Agreement** | `.pdf` (3 pages) / `.txt` | Enterprise B2B contract with Scope of Work, Net 30 Invoicing, 1.5% Late Interest, 60-Day Termination for Convenience, IP Ownership, Mutual NDA, IP Indemnification, 12-Month Liability Cap, and Arbitration in Lahore under the Arbitration Act, 1940. |
| **Mutual Non-Disclosure Agreement** | `.pdf` (2 pages) / `.txt` | Bilateral confidentiality contract with standard trade secret definitions, 4 exclusions, standard of care, compelled disclosure notice, return/destruction within 10 days, and court injunctive relief. |
| **Residential Tenancy Lease Agreement** | `.pdf` (2 pages) / `.txt` | Real estate lease (*Kirayanama*) with PKR 150,000 monthly rent, PKR 300,000 security deposit, 10% annual escalation, tenant maintenance duties, and eviction procedures under the Punjab Rented Premises Act. |

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/LegalDocAiAssist.git
cd LegalDocAiAssist
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
Copy the template and add your API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY=AIzaSy...your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
```
*(Note: You can also enter or test your Gemini API Key directly inside the application sidebar at runtime!)*

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud Deployment

Deploying LegalDocAiAssist to **Streamlit Community Cloud** takes less than 3 minutes:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "feat: LegalDocAiAssist v1.0 release"
   git push origin main
   ```
2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io/).
   - Click **"New app"** and select your `LegalDocAiAssist` repository and branch `main`.
   - Set **Main file path** to `app.py`.
3. **Configure Secrets**:
   - In your app settings on Streamlit Cloud, navigate to **Settings > Secrets**.
   - Enter your Gemini API credentials:
     ```toml
     GEMINI_API_KEY = "AIzaSyYourGeminiApiKeyHere"
     GEMINI_MODEL = "gemini-2.5-flash"
     ```
4. **Click Deploy**: Streamlit Cloud will install all dependencies from `requirements.txt` and launch your live application with TLS encryption.

---

## 🧪 Comprehensive Automated Test Suite

The test suite in [`tests/test_pipeline.py`](file:///c:/Projects/Development/LegalDocAIAssist/tests/test_pipeline.py) verifies all core subsystems:

```bash
python tests/test_pipeline.py
```

### Verified Test Cases:
- `test_01_unsupported_file_format`: Rejects unapproved file extensions gracefully.
- `test_02_empty_text_handling`: Handles 0-byte or whitespace-only documents cleanly.
- `test_03_legal_qualifiers_preservation`: Preserves all negations and qualifiers (`shall not`, `unless`, `must`).
- `test_04_clause_aware_chunking`: Validates section headers, clause numbers, and metadata preservation.
- `test_05_contract_attention_indicators`: Detects the 7 key provisions and generates citation metrics.
- `test_06_embeddings_dimension_and_norm`: Validates MiniLM 384-d dense vectors and L2 unit normalization.
- `test_07_faiss_document_index_retrieval`: Validates IndexFlatIP cosine similarity and top-K search.
- `test_08_general_legal_knowledge_base`: Verifies knowledge base indexing and concept retrieval.
- `test_09_two_source_rag_retrieval`: Tests simultaneous retrieval from document and knowledge base.
- `test_10_grounded_generation_english_format`: Enforces standard Section 14 headers in English output.
- `test_11_grounded_generation_urdu_format`: Verifies native Urdu script and contractual phrasing.
- `test_12_anti_hallucination_on_unanswerable_query`: Enforces anti-hallucination message when evidence is missing.
- `test_13_expanded_knowledge_base_depth`: Asserts 70+ terms, 50+ clauses, and 8+ statutory forms.
- `test_14_sample_documents_pipeline`: Verifies full multi-page PDF contract ingestion and clause chunking.
- `test_15_plain_text_document_support`: Verifies ingestion of `.txt` and `.md` legal documents.

**Current Test Result:** `Ran 15 tests in 0.205s - OK (100% passing)`

---

## 🛡️ Jurisdiction Safety & Ethical Guidelines

- **Zero Jurisdiction Hallucination**: The system **never fabricates or guesses** local statutes, section numbers, or court precedents.
- **Evidence-First Guarantee**: If an answer cannot be deduced with high confidence from the uploaded text or indexed knowledge, the assistant explicitly states that evidence is insufficient.
- **Neutral & Objective Phrasing**: Responses use objective contractual phrasing (*"Section 3.2 indicates..."*, *"The document states that..."*) rather than subjective assertions.
- **Prominent Disclaimers**: Every generated explanation card and downloadable report prominently includes the mandatory educational disclaimer.

---

## 📄 License & Attribution

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details. Built with Google Gemini, Streamlit, FAISS, and Sentence Transformers.
