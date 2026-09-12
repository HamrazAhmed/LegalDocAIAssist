"""
General Legal Knowledge Base Module for LegalDocAiAssist.

Loads and indexes curated educational legal knowledge:
- 50 common legal and contractual terms (bilingual: English & Urdu)
- 36 standard contractual clauses with definitions and risk factors
- Educational government form guidance

Implements dedicated FAISS knowledge index for general legal concepts.
Design supports future modular datasets (e.g. /pakistan) without altering core retrieval.
"""

import os
import json
from typing import List, Dict, Any, Optional

from modules.embeddings import FaissIndexManager, create_faiss_index

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base")

_CACHED_TERMS: Optional[List[Dict[str, Any]]] = None
_CACHED_CLAUSES: Optional[List[Dict[str, Any]]] = None
_CACHED_FORMS: Optional[List[Dict[str, Any]]] = None
_CACHED_KNOWLEDGE_INDEX: Optional[FaissIndexManager] = None


def load_legal_terms() -> List[Dict[str, Any]]:
    """Loads curated legal terms from legal_terms.json."""
    global _CACHED_TERMS
    if _CACHED_TERMS is not None:
        return _CACHED_TERMS

    path = os.path.join(KB_DIR, "legal_terms.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            _CACHED_TERMS = json.load(f)
    else:
        _CACHED_TERMS = []
    return _CACHED_TERMS


def load_common_clauses() -> List[Dict[str, Any]]:
    """Loads curated common clauses from common_clauses.json."""
    global _CACHED_CLAUSES
    if _CACHED_CLAUSES is not None:
        return _CACHED_CLAUSES

    path = os.path.join(KB_DIR, "common_clauses.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            _CACHED_CLAUSES = json.load(f)
    else:
        _CACHED_CLAUSES = []
    return _CACHED_CLAUSES


def load_government_forms() -> List[Dict[str, Any]]:
    """Loads educational government form guidelines from government_forms.json."""
    global _CACHED_FORMS
    if _CACHED_FORMS is not None:
        return _CACHED_FORMS

    path = os.path.join(KB_DIR, "government_forms.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            _CACHED_FORMS = json.load(f)
    else:
        _CACHED_FORMS = []
    return _CACHED_FORMS


def build_knowledge_chunks() -> List[Dict[str, Any]]:
    """
    Combines terms, clauses, and form templates into normalized chunk representations
    for semantic FAISS vector retrieval.
    """
    chunks: List[Dict[str, Any]] = []

    # 1. Legal Terms
    terms = load_legal_terms()
    for idx, t in enumerate(terms):
        term_name = t.get("term", "")
        category = t.get("category", "General")
        definition = t.get("definition", "")
        simple_eng = t.get("simple_english", "")
        simple_urdu = t.get("simple_urdu", "")
        note = t.get("important_note", "")
        aliases = ", ".join(t.get("aliases", []))

        text_representation = (
            f"Legal Term: {term_name} (Category: {category})\n"
            f"Definition: {definition}\n"
            f"Plain English Meaning: {simple_eng}\n"
            f"Urdu Meaning: {simple_urdu}\n"
            f"Important Legal Note: {note}\n"
            f"Related Terms: {aliases}"
        )

        chunks.append({
            "chunk_id": f"kb_term_{idx + 1}",
            "text": text_representation,
            "title": term_name,
            "category": category,
            "item_type": "legal_term",
            "simple_english": simple_eng,
            "simple_urdu": simple_urdu,
            "important_note": note,
            "source": "legal_knowledge_base"
        })

    # 2. Common Clauses
    clauses = load_common_clauses()
    for idx, c in enumerate(clauses):
        clause_name = c.get("clause", "")
        category = c.get("category", "General")
        meaning = c.get("meaning", "")
        simple_eng = c.get("simple_english", "")
        simple_urdu = c.get("simple_urdu", "")
        what_to_look_for = c.get("what_to_look_for", "")

        text_representation = (
            f"Contract Clause: {clause_name} (Category: {category})\n"
            f"Legal Meaning: {meaning}\n"
            f"Plain English: {simple_eng}\n"
            f"Urdu: {simple_urdu}\n"
            f"Key Things To Check / Risks: {what_to_look_for}"
        )

        chunks.append({
            "chunk_id": f"kb_clause_{idx + 1}",
            "text": text_representation,
            "title": clause_name,
            "category": category,
            "item_type": "common_clause",
            "simple_english": simple_eng,
            "simple_urdu": simple_urdu,
            "what_to_look_for": what_to_look_for,
            "source": "legal_knowledge_base"
        })

    # 3. Government Forms
    forms = load_government_forms()
    for idx, gf in enumerate(forms):
        form_name = gf.get("form_type", "")
        purpose = gf.get("purpose", "")
        docs = ", ".join(gf.get("typical_supporting_docs", []))
        notes = gf.get("important_notes", "")

        text_representation = (
            f"Legal/Government Form: {form_name}\n"
            f"Purpose: {purpose}\n"
            f"Typical Supporting Documents: {docs}\n"
            f"Important Notes: {notes}"
        )

        chunks.append({
            "chunk_id": f"kb_form_{idx + 1}",
            "text": text_representation,
            "title": form_name,
            "category": "Government Form",
            "item_type": "government_form",
            "simple_english": purpose,
            "source": "legal_knowledge_base"
        })

    return chunks


def get_legal_knowledge_index() -> FaissIndexManager:
    """
    Returns the singleton FAISS index for general legal knowledge.
    Builds and embeds the index on first invocation.
    """
    global _CACHED_KNOWLEDGE_INDEX
    if _CACHED_KNOWLEDGE_INDEX is not None:
        return _CACHED_KNOWLEDGE_INDEX

    chunks = build_knowledge_chunks()
    _CACHED_KNOWLEDGE_INDEX = create_faiss_index(chunks)
    return _CACHED_KNOWLEDGE_INDEX


def search_legal_knowledge(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves top_k relevant educational concepts from the general legal knowledge index.
    """
    index = get_legal_knowledge_index()
    return index.search(query, top_k=top_k)
