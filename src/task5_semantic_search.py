"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Phải tương thích với embedding model và vector store ở Task 4
"""

from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .task4_chunking_indexing import chunk_documents, load_documents


@lru_cache(maxsize=1)
def _build_index():
    chunks = chunk_documents(load_documents())
    if not chunks:
        return [], None, None

    vectorizer = TfidfVectorizer(
        lowercase=True,
        analyzer="word",
        ngram_range=(1, 2),
        max_features=20000,
    )
    matrix = vectorizer.fit_transform([c["content"] for c in chunks])
    return chunks, vectorizer, matrix


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score
            'metadata': dict     # source, doc_type, chunk_index
        }
        Sorted by score descending.
    """
    chunks, vectorizer, matrix = _build_index()
    if not chunks or not query.strip():
        return []

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).ravel()
    ranked = scores.argsort()[::-1][:top_k]

    results = []
    for idx in ranked:
        score = float(scores[idx])
        if score <= 0:
            continue
        chunk = chunks[int(idx)]
        results.append({
            "content": chunk["content"],
            "score": score,
            "metadata": chunk["metadata"],
        })
    return results


if __name__ == "__main__":
    # Test
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
