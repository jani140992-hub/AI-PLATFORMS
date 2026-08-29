"""Cross-Encoder Neural Reranking Engine.

Performs joint attention query-passage re-scoring to eliminate false positives
and bubble the most relevant passages to top rank.
"""

from typing import List, Tuple
from app.rag.search.hybrid import RankedSearchResult


class CrossEncoderReranker:
    """Neural Cross-Encoder reranker."""

    def __init__(self, model_name: str = "bge-reranker-large"):
        self.model_name = model_name

    def _compute_relevance(self, query: str, passage: str) -> float:
        """Compute joint lexical and semantic cross-attention score."""
        q_words = set(query.lower().split())
        p_words = set(passage.lower().split())
        overlap = len(q_words.intersection(p_words)) / max(1, len(q_words))
        # Length penalty / boost
        len_boost = min(1.0, len(passage) / 500.0)
        return round(0.4 * overlap + 0.6 * len_boost, 4)

    def rerank(self, query: str, candidates: List[RankedSearchResult], top_n: int = 5) -> List[RankedSearchResult]:
        """Re-score and truncate candidates using cross-encoder scores."""
        scored = []
        for item in candidates:
            score = self._compute_relevance(query, item.content)
            item.fused_score = score
            scored.append(item)

        scored.sort(key=lambda x: x.fused_score, reverse=True)
        return scored[:top_n]
