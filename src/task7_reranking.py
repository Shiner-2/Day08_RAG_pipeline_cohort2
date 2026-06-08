"""
Task 7 — Reranking Module.

Local implementation dùng token-overlap reranking và RRF. Cách này nhẹ, chạy
offline, và đủ để demo cơ chế rerank sau bước retrieval.
"""

import re


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower(), flags=re.UNICODE))


def rerank_cross_encoder(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """Offline cross-encoder substitute: combine query overlap with old score."""
    query_tokens = _tokens(query)
    rescored = []
    for item in candidates:
        doc_tokens = _tokens(item.get("content", ""))
        overlap = len(query_tokens & doc_tokens) / max(len(query_tokens), 1)
        base_score = float(item.get("score", 0.0))
        new_item = item.copy()
        new_item["score"] = 0.7 * overlap + 0.3 * base_score
        rescored.append(new_item)
    return sorted(rescored, key=lambda x: x["score"], reverse=True)[:top_k]


def rerank_mmr(
    query_embedding: list[float],
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """Minimal MMR-compatible fallback for candidates without embeddings."""
    return sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)[:top_k]


def rerank_rrf(ranked_lists: list[list[dict]], top_k: int = 5, k: int = 60) -> list[dict]:
    """Reciprocal Rank Fusion over multiple ranked lists."""
    rrf_scores: dict[str, float] = {}
    content_map: dict[str, dict] = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            key = item["content"]
            rrf_scores[key] = rrf_scores.get(key, 0.0) + 1 / (k + rank)
            content_map[key] = item

    results = []
    for content, score in sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]:
        item = content_map[content].copy()
        item["score"] = float(score)
        results.append(item)
    return results


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "cross_encoder",
) -> list[dict]:
    """Unified reranking interface."""
    if method == "cross_encoder":
        return rerank_cross_encoder(query, candidates, top_k)
    if method == "mmr":
        return rerank_cross_encoder(query, candidates, top_k)
    if method == "rrf":
        return rerank_rrf([candidates], top_k=top_k)
    raise ValueError(f"Unknown rerank method: {method}")


if __name__ == "__main__":
    dummy_candidates = [
        {"content": "Điều 248: Tội tàng trữ trái phép chất ma tuý", "score": 0.8, "metadata": {}},
        {"content": "Nghệ sĩ X bị bắt vì sử dụng ma tuý", "score": 0.7, "metadata": {}},
        {"content": "Hình phạt tù từ 2-7 năm cho tội tàng trữ", "score": 0.6, "metadata": {}},
    ]
    for r in rerank("hình phạt tàng trữ ma tuý", dummy_candidates, top_k=2):
        print(f"[{r['score']:.3f}] {r['content']}")
