"""
Comprehensive End-to-End Test Suite for LegalDocAiAssist (Section 21 Compliance).

Covers all 12 core test requirements:
1. Unsupported file format rejection
2. Empty document handling
3. Legal text cleaning & qualifier preservation
4. Clause-aware chunking & metadata integrity
5. Contract attention indicators
6. MiniLM 384-d embeddings & normalization
7. FAISS document indexing & retrieval
8. General legal knowledge base retrieval
9. Two-source RAG retrieval integration
10. Grounded English generation formatting
11. Grounded Urdu generation with proper script
12. Anti-hallucination verification on unanswerable queries
"""

import sys
import os
import unittest
import numpy as np

# Ensure root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from modules.document_processor import (
    clean_legal_text,
    process_document,
    chunk_document_sections,
    detect_key_clauses_summary,
)
from modules.embeddings import (
    embed_text,
    embed_batch,
    create_faiss_index,
    get_embedding_dimension,
)
from modules.knowledge_base import (
    load_legal_terms,
    load_common_clauses,
    load_government_forms,
    search_legal_knowledge,
)
from modules.rag import (
    retrieve_rag_context,
    generate_grounded_explanation,
    test_gemini_connection,
)


class TestLegalDocAiAssistPipeline(unittest.TestCase):

    def test_01_unsupported_file_format(self):
        """Test that invalid/unsupported file types fail gracefully with ValueError."""
        with self.assertRaises(ValueError) as ctx:
            process_document(b"random bytes", "contract.exe")
        self.assertIn("Unsupported file format", str(ctx.exception))

    def test_02_empty_text_handling(self):
        """Test clean_legal_text on empty, whitespace-only, and null strings."""
        self.assertEqual(clean_legal_text(""), "")
        self.assertEqual(clean_legal_text("   \n\n\t  "), "")

    def test_03_legal_qualifiers_preservation(self):
        """Test that critical legal qualifiers and negation words are never stripped."""
        raw_clause = (
            "8.2 Termination. The Company shall not be liable, and may immediately terminate "
            "without penalty if Contractor breaches confidentiality, unless authorized in writing, "
            "and all deliverables must be returned except as prohibited by law."
        )
        cleaned = clean_legal_text(raw_clause)
        for keyword in ["shall not", "without", "unless", "must", "except", "prohibited"]:
            self.assertIn(keyword, cleaned, f"Keyword '{keyword}' must be preserved.")

    def test_04_clause_aware_chunking(self):
        """Test clause-aware chunking for section headers, clause numbers, and metadata."""
        sample_sections = [{
            "text": "8. Termination\n\n8.1 Either party may terminate with 30 days notice.\n\n8.2 Immediate breach termination.",
            "page": 4,
            "section": "General",
            "source_type": "digital_pdf",
            "file_name": "master_agreement.pdf"
        }]
        chunks = chunk_document_sections(sample_sections)
        self.assertGreaterEqual(len(chunks), 2)
        
        # Check metadata schema
        for c in chunks:
            self.assertEqual(c["page"], 4)
            self.assertEqual(c["source"], "uploaded_document")
            self.assertEqual(c["file_name"], "master_agreement.pdf")
            self.assertIn("8. Termination", c["section"])

        clauses = [c["clause"] for c in chunks]
        self.assertTrue(any("8.1" in cl or "8.2" in cl for cl in clauses))

    def test_05_contract_attention_indicators(self):
        """Test automated detection of key contractual provisions and attention metrics."""
        chunks = [
            {"text": "Section 8. Termination. Notice of 30 days.", "section": "8. Termination", "clause": "8.1", "page": 4},
            {"text": "Section 10. Indemnification and Hold Harmless obligations.", "section": "10. Indemnity", "clause": "10.1", "page": 6},
            {"text": "Section 12. Limitation of Liability cap.", "section": "12. Liability", "clause": "12.1", "page": 7}
        ]
        indicators = detect_key_clauses_summary(chunks)
        self.assertTrue(indicators["indicators"]["Termination Clause"])
        self.assertTrue(indicators["indicators"]["Indemnity / Hold Harmless"])
        self.assertTrue(indicators["indicators"]["Limitation of Liability"])
        self.assertFalse(indicators["indicators"]["Governing Law & Jurisdiction"])
        self.assertGreater(indicators["total_words"], 10)

    def test_06_embeddings_dimension_and_norm(self):
        """Test MiniLM 384-dimensional dense vectors and L2 unit normalization."""
        dim = get_embedding_dimension()
        self.assertEqual(dim, 384)

        vec = embed_text("Contractual obligation under applicable law.")
        self.assertEqual(vec.shape, (384,))
        self.assertEqual(vec.dtype, np.float32)
        norm = np.linalg.norm(vec)
        self.assertTrue(np.isclose(norm, 1.0, atol=1e-3))

    def test_07_faiss_document_index_retrieval(self):
        """Test building FAISS index and retrieving top-K semantic results."""
        chunks = [
            {"chunk_id": "c1", "text": "Section 8. Termination with thirty days notice.", "page": 4, "clause": "8.1", "section": "Termination"},
            {"chunk_id": "c2", "text": "Section 5. Invoices must be paid Net 30 days.", "page": 2, "clause": "5.1", "section": "Payment"},
            {"chunk_id": "c3", "text": "Section 14. Both parties agree to arbitration in London.", "page": 9, "clause": "14.1", "section": "Disputes"}
        ]
        index = create_faiss_index(chunks)
        self.assertEqual(index.count(), 3)

        results = index.search("How do I cancel or terminate early?", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["clause"], "8.1")
        self.assertIn("score", results[0])

    def test_08_general_legal_knowledge_base(self):
        """Test knowledge base dataset sizes (40+ terms, 30+ clauses) and search."""
        terms = load_legal_terms()
        clauses = load_common_clauses()
        forms = load_government_forms()

        self.assertGreaterEqual(len(terms), 40, "Must have at least 40 terms.")
        self.assertGreaterEqual(len(clauses), 30, "Must have at least 30 clauses.")
        self.assertGreaterEqual(len(forms), 3, "Must have educational forms.")

        kb_search_res = search_legal_knowledge("What is force majeure?", top_k=1)
        self.assertGreater(len(kb_search_res), 0)
        self.assertIn("Force Majeure", kb_search_res[0]["title"])

    def test_09_two_source_rag_retrieval(self):
        """Test simultaneous retrieval across document chunks and legal knowledge."""
        chunks = [{
            "chunk_id": "doc_1",
            "text": "8.2 Termination for Cause upon material breach.",
            "page": 4,
            "section": "8. Termination",
            "clause": "8.2",
            "source": "uploaded_document"
        }]
        doc_index = create_faiss_index(chunks)

        rag_payload = retrieve_rag_context("terminate for breach", doc_index=doc_index, top_k_doc=1, top_k_kb=1)
        self.assertEqual(len(rag_payload["doc_chunks"]), 1)
        self.assertEqual(len(rag_payload["kb_chunks"]), 1)
        self.assertIn("PRIMARY EVIDENCE", rag_payload["formatted_context"])
        self.assertIn("SECONDARY CONTEXT", rag_payload["formatted_context"])

    def test_10_grounded_generation_english_format(self):
        """Test that English generation strictly produces all Section 14 headers."""
        payload = {
            "doc_chunks": [{"page": 4, "section": "8. Termination", "clause": "8.2", "text": "Immediate termination on breach."}],
            "kb_chunks": [{"title": "Breach", "simple_english": "Breaking contract rules.", "simple_urdu": "خلاف ورزی۔"}],
            "formatted_context": "Sample context"
        }
        res = generate_grounded_explanation("What happens if there is a breach?", payload, language="English")
        text = res["text"]
        for header in ["DOCUMENT OVERVIEW", "KEY POINTS", "IMPORTANT CLAUSES", "LEGAL TERMS", "SOURCE"]:
            self.assertIn(header, text, f"Response must include header '{header}'")

    def test_11_grounded_generation_urdu_format(self):
        """Test that Urdu generation produces proper Urdu script and mentions clauses."""
        payload = {
            "doc_chunks": [{"page": 4, "section": "8. Termination", "clause": "8.2", "text": "Immediate termination on breach."}],
            "kb_chunks": [{"title": "Breach", "simple_english": "Breaking contract rules.", "simple_urdu": "خلاف ورزی۔"}],
            "formatted_context": "Sample context"
        }
        res = generate_grounded_explanation("What happens if there is a breach?", payload, language="Urdu")
        text = res["text"]
        self.assertIn("DOCUMENT OVERVIEW", text)
        self.assertTrue("صفحہ" in text or "شق" in text or "معاہدہ" in text)

    def test_12_anti_hallucination_on_unanswerable_query(self):
        """Test anti-hallucination safeguard when document has no matching evidence."""
        empty_payload = {"doc_chunks": [], "kb_chunks": [], "formatted_context": ""}
        res = generate_grounded_explanation("What is the director's personal mobile number?", empty_payload, language="English")
        self.assertIn("not mentioned or cannot be definitively determined", res["text"])

    def test_13_expanded_knowledge_base_depth(self):
        """Test that expanded knowledge base has 70+ terms, 50+ clauses, and 8+ forms."""
        terms = load_legal_terms()
        clauses = load_common_clauses()
        forms = load_government_forms()

        self.assertGreaterEqual(len(terms), 70, f"Expected 70+ terms, got {len(terms)}")
        self.assertGreaterEqual(len(clauses), 50, f"Expected 50+ clauses, got {len(clauses)}")
        self.assertGreaterEqual(len(forms), 8, f"Expected 8+ forms, got {len(forms)}")

        # Verify specific high-value terms added
        term_names = {t["term"] for t in terms}
        for expected in ["Liquidated Damages", "Specific Performance", "Promissory Estoppel", "Caveat Emptor"]:
            self.assertIn(expected, term_names)

        # Verify specific high-value clauses added
        clause_names = {c["clause"] for c in clauses}
        for expected in ["Audit and Inspection Rights", "Non-Disparagement", "Cumulative Remedies"]:
            self.assertIn(expected, clause_names)

    def test_14_sample_documents_pipeline(self):
        """Test processing real sample contracts from sample_documents directory."""
        sample_path = os.path.join(ROOT_DIR, "sample_documents", "commercial_services_agreement.pdf")
        self.assertTrue(os.path.exists(sample_path), "Sample MSA must exist.")

        with open(sample_path, "rb") as f:
            pdf_bytes = f.read()

        sections = process_document(pdf_bytes, "commercial_services_agreement.pdf")
        self.assertGreaterEqual(len(sections), 1, "Must extract at least 1 section from sample PDF.")
        
        chunks = chunk_document_sections(sections)
        self.assertGreaterEqual(len(chunks), 5, "Must extract multiple clause chunks.")
        
        # Test provision indicators
        indicators = detect_key_clauses_summary(chunks)
        self.assertTrue(indicators["indicators"]["Termination Clause"])
        self.assertTrue(indicators["indicators"]["Limitation of Liability"])

    def test_15_plain_text_document_support(self):
        """Test that .txt and .md legal documents are properly ingested and processed."""
        txt_path = os.path.join(ROOT_DIR, "sample_documents", "mutual_non_disclosure_agreement.txt")
        self.assertTrue(os.path.exists(txt_path), "Sample NDA text must exist.")

        with open(txt_path, "r", encoding="utf-8") as f:
            txt_content = f.read()

        sections = process_document(txt_content, "mutual_non_disclosure_agreement.txt")
        self.assertGreaterEqual(len(sections), 1)
        chunks = chunk_document_sections(sections)
        self.assertGreaterEqual(len(chunks), 3)


if __name__ == "__main__":
    unittest.main()

