"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25. Nếu dùng phương pháp khác (TF-IDF, Elasticsearch,
Weaviate BM25 built-in), hãy giải thích cơ chế trong buổi demo → +5 bonus.

Cài đặt:
    pip install rank-bm25

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

from pathlib import Path
import math
import re

from .task4_chunking_indexing import chunk_documents, load_documents

# TODO: Load corpus từ data/standardized/ hoặc từ vector store
CORPUS: list[dict] = []  # List of {'content': str, 'metadata': dict}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def build_bm25_index(corpus: list[dict]):
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}
    """
    tokenized = [_tokenize(doc["content"]) for doc in corpus]
    doc_freq: dict[str, int] = {}
    for tokens in tokenized:
        for token in set(tokens):
            doc_freq[token] = doc_freq.get(token, 0) + 1
    avgdl = sum(len(tokens) for tokens in tokenized) / max(len(tokenized), 1)
    return {"tokenized": tokenized, "df": doc_freq, "avgdl": avgdl, "n": len(tokenized)}


def _load_corpus() -> list[dict]:
    global CORPUS
    if not CORPUS:
        CORPUS = chunk_documents(load_documents())
    return CORPUS


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,      # BM25 score
            'metadata': dict
        }
        Sorted by score descending.
    """
    corpus = _load_corpus()
    if not corpus or not query.strip():
        return []

    index = build_bm25_index(corpus)
    query_tokens = _tokenize(query)
    k1 = 1.5
    b = 0.75
    scores = []

    for tokens in index["tokenized"]:
        dl = len(tokens)
        tf: dict[str, int] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1

        score = 0.0
        for token in query_tokens:
            if token not in tf:
                continue
            df = index["df"].get(token, 0)
            idf = math.log(1 + (index["n"] - df + 0.5) / (df + 0.5))
            denom = tf[token] + k1 * (1 - b + b * dl / max(index["avgdl"], 1))
            score += idf * (tf[token] * (k1 + 1)) / denom
        scores.append(score)

    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    results = []
    for idx in ranked:
        if scores[idx] <= 0:
            continue
        results.append({
            "content": corpus[idx]["content"],
            "score": float(scores[idx]),
            "metadata": corpus[idx]["metadata"],
        })
    return results


if __name__ == "__main__":
    # Test
    results = lexical_search("Điều 248 tàng trữ trái phép chất ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
