"""
Embeddings Pipeline Module for LegalDocAiAssist.

Provides dense semantic vector representations using the all-MiniLM-L6-v2 model.
Produces normalized 384-dimensional vectors for FAISS cosine similarity indexing.
Includes graceful fallback for seamless offline testing when sentence-transformers is not yet installed.
"""

from typing import List, Dict, Any, Optional
import hashlib
import numpy as np

# Try importing Streamlit for cache_resource
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Try importing sentence_transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

# Try importing faiss
try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Module-level singleton cache
_GLOBAL_MODEL_CACHE: Optional[Any] = None


def _load_model() -> Any:
    """Internal loader for SentenceTransformer with all-MiniLM-L6-v2."""
    if not HAS_SENTENCE_TRANSFORMERS:
        return None
    return SentenceTransformer(MODEL_NAME)


# Decorate with st.cache_resource if running inside Streamlit
if HAS_STREAMLIT:
    get_embedding_model = st.cache_resource(show_spinner="Loading all-MiniLM-L6-v2 embeddings model...")(_load_model)
else:
    def get_embedding_model() -> Any:
        global _GLOBAL_MODEL_CACHE
        if _GLOBAL_MODEL_CACHE is None:
            _GLOBAL_MODEL_CACHE = _load_model()
        return _GLOBAL_MODEL_CACHE


def get_embedding_dimension() -> int:
    """Returns the vector dimensionality (384 for all-MiniLM-L6-v2)."""
    return EMBEDDING_DIM


def _fallback_embed_batch(texts: List[str]) -> np.ndarray:
    """
    Deterministic 384-d normalized vector representation used when sentence-transformers
    is not installed locally. Employs subword n-gram feature hashing to capture morphological
    matches (e.g. 'terminate' <-> 'termination') while preserving 384-d unit normalization.
    """
    import re
    stopwords = {"the", "a", "an", "is", "in", "at", "of", "and", "or", "to", "for", "with", "how", "do", "i", "by"}
    vectors = []

    for t in texts:
        vec = np.zeros(EMBEDDING_DIM, dtype=np.float32)
        clean_t = re.sub(r'[^\w\s]', ' ', t.lower())
        raw_words = clean_t.split()
        words = [w for w in raw_words if w not in stopwords] or raw_words

        if not words:
            vectors.append(vec)
            continue

        for word in words:
            # Full word feature (higher weight)
            h_word = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            vec[h_word % EMBEDDING_DIM] += 2.5

            # Subword n-grams (3 to 5 chars) for morphological matching
            for n in (3, 4, 5):
                if len(word) >= n:
                    for i in range(len(word) - n + 1):
                        ngram = word[i:i+n]
                        h_ng = int(hashlib.md5(ngram.encode("utf-8")).hexdigest(), 16)
                        vec[h_ng % EMBEDDING_DIM] += 1.0

        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec = vec / norm
        vectors.append(vec)

    return np.vstack(vectors).astype(np.float32)


def embed_text(text: str) -> np.ndarray:
    """
    Generate normalized 384-dimensional float32 vector embedding for a single text.
    L2 normalization ensures dot product equals cosine similarity in FAISS IndexFlatIP.
    """
    if not text or not text.strip():
        return np.zeros(EMBEDDING_DIM, dtype=np.float32)

    if HAS_SENTENCE_TRANSFORMERS:
        try:
            model = get_embedding_model()
            if model is not None:
                vector = model.encode(text, normalize_embeddings=True, convert_to_numpy=True)
                return vector.astype(np.float32)
        except Exception:
            pass

    # Use deterministic fallback
    return _fallback_embed_batch([text])[0]


def embed_batch(
    texts: List[str],
    batch_size: int = 32,
    show_progress: bool = False
) -> np.ndarray:
    """
    Generate normalized 384-dimensional float32 embeddings for a batch of texts.
    Returns:
        np.ndarray of shape (len(texts), 384), dtype=float32
    """
    if not texts:
        return np.empty((0, EMBEDDING_DIM), dtype=np.float32)

    sanitized = [t if t and t.strip() else " " for t in texts]

    if HAS_SENTENCE_TRANSFORMERS:
        try:
            model = get_embedding_model()
            if model is not None:
                embeddings = model.encode(
                    sanitized,
                    batch_size=batch_size,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=show_progress
                )
                return embeddings.astype(np.float32)
        except Exception:
            pass

    return _fallback_embed_batch(sanitized)


def embed_document_chunks(
    chunks: List[Dict[str, Any]],
    batch_size: int = 32
) -> np.ndarray:
    """
    Extracts text from a list of document chunk dicts and produces a 2D float32 embedding matrix.
    Each chunk dict must have a 'text' field.
    Returns:
        np.ndarray of shape (len(chunks), 384), dtype=float32
    """
    if not chunks:
        return np.empty((0, EMBEDDING_DIM), dtype=np.float32)

    texts = [c.get("text", "") for c in chunks]
    return embed_batch(texts, batch_size=batch_size)


class FaissIndexManager:
    """
    FAISS-powered semantic index for legal document clauses and knowledge chunks.
    Uses Inner Product (IndexFlatIP) on L2-normalized vectors for exact cosine similarity ranking.
    Maintains 1-to-1 mapping with chunk metadata for accurate clause and source attribution.
    """

    def __init__(self, dimension: int = EMBEDDING_DIM):
        self.dimension = dimension
        self.index = None
        self.chunks_metadata: List[Dict[str, Any]] = []
        self._fallback_matrix: Optional[np.ndarray] = None
        self._reset_index()

    def _reset_index(self):
        """Initializes or resets the underlying index."""
        self.chunks_metadata = []
        if HAS_FAISS:
            self.index = faiss.IndexFlatIP(self.dimension)
            self._fallback_matrix = None
        else:
            self.index = None
            self._fallback_matrix = np.empty((0, self.dimension), dtype=np.float32)

    def count(self) -> int:
        """Returns total number of indexed vectors."""
        return len(self.chunks_metadata)

    def add_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 32) -> int:
        """
        Embeds and adds chunks to the FAISS index.
        Attaches internal metadata mappings for retrieval.
        Returns:
            Number of chunks successfully indexed.
        """
        if not chunks:
            return 0

        vectors = embed_document_chunks(chunks, batch_size=batch_size)
        if len(vectors) == 0:
            return 0

        if HAS_FAISS and self.index is not None:
            vectors_c = np.ascontiguousarray(vectors, dtype=np.float32)
            self.index.add(vectors_c)
        else:
            if self._fallback_matrix is None or len(self._fallback_matrix) == 0:
                self._fallback_matrix = vectors
            else:
                self._fallback_matrix = np.vstack([self._fallback_matrix, vectors])

        self.chunks_metadata.extend(chunks)
        return len(chunks)

    def search_by_vector(
        self,
        query_vector: np.ndarray,
        top_k: int = 4,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Searches index with an embedding vector and returns top_k nearest chunks with scores.
        """
        if self.count() == 0:
            return []

        actual_k = min(top_k, self.count())
        results: List[Dict[str, Any]] = []

        if HAS_FAISS and self.index is not None:
            query_2d = np.ascontiguousarray(query_vector.reshape(1, -1), dtype=np.float32)
            scores, indices = self.index.search(query_2d, actual_k)
            matched_indices = indices[0]
            matched_scores = scores[0]
        else:
            # Fallback exact cosine inner-product
            sims = np.dot(self._fallback_matrix, query_vector)
            top_indices = np.argsort(sims)[::-1][:actual_k]
            matched_indices = top_indices
            matched_scores = sims[top_indices]

        for idx, score in zip(matched_indices, matched_scores):
            if idx < 0 or idx >= len(self.chunks_metadata):
                continue
            if score < score_threshold:
                continue

            chunk_copy = dict(self.chunks_metadata[idx])
            chunk_copy["score"] = round(float(score), 4)
            results.append(chunk_copy)

        return results

    def search(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Convenience method: Embeds query text and retrieves top_k relevant chunks.
        """
        if not query or not query.strip() or self.count() == 0:
            return []

        q_vec = embed_text(query)
        return self.search_by_vector(q_vec, top_k=top_k, score_threshold=score_threshold)


def create_faiss_index(chunks: List[Dict[str, Any]]) -> FaissIndexManager:
    """Factory helper to build a populated FaissIndexManager from a list of chunks."""
    manager = FaissIndexManager()
    manager.add_chunks(chunks)
    return manager

