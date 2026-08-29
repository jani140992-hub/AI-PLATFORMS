"""Reciprocal Rank Fusion (RRF) and Hybrid Search Pipeline.

Fuses dense semantic similarity rankings with sparse BM25 lexical rankings
to produce an optimized final retrieval candidate list.
"""

from typing import Dict, List, Tuple
from pydantic import BaseModel


class RankedSearchResult(BaseModel):
    """Unified search result entry."""

    chunk_id: str
    dense_score: float = 0.0
    bm25_score: float = 0.0
    fused_score: float = 0.0
    content: str = ""
    metadata: Dict[str, Any] = {}


class HybridSearchPipeline:
    """Fuses multi-modal search candidates using Reciprocal Rank Fusion."""

    def __init__(self, rrf_k: int = 60, dense_weight: float = 0.5, sparse_weight: float = 0.5):
        self.rrf_k = rrf_k
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight

    def reciprocal_rank_fusion(
        self,
        dense_results: List[Tuple[str, float, str, Dict[str, Any]]],  # (chunk_id, score, content, meta)
        bm25_results: List[Tuple[str, float]],                         # (chunk_id, score)
        top_k: int = 10,
    ) -> List[RankedSearchResult]:
        """Combine dense and sparse lists using RRF algorithm: score = sum(1 / (k + rank))."""
        fused_scores: Dict[str, float] = {}
        content_map: Dict[str, Tuple[str, Dict[str, Any]]] = {}
        dense_score_map: Dict[str, float] = {}
        bm25_score_map: Dict[str, float] = {}

        # Process Dense ranks
        for rank, (chunk_id, score, content, meta) in enumerate(dense_results):
            fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + (self.dense_weight / (self.rrf_k + rank + 1))
            dense_score_map[chunk_id] = score
            content_map[chunk_id] = (content, meta)

        # Process BM25 ranks
        for rank, (chunk_id, score) in enumerate(bm25_results):
            fused_scores[chunk_id] = fused_scores.get(chunk_id, 0.0) + (self.sparse_weight / (self.rrf_k + rank + 1))
            bm25_score_map[chunk_id] = score

        # Sort by fused score
        sorted_chunks = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for chunk_id, f_score in sorted_chunks:
            content, meta = content_map.get(chunk_id, ("", {}))
            results.append(
                RankedSearchResult(
                    chunk_id=chunk_id,
                    dense_score=dense_score_map.get(chunk_id, 0.0),
                    bm25_score=bm25_score_map.get(chunk_id, 0.0),
                    fused_score=f_score,
                    content=content,
                    metadata=meta,
                )
            )

        return results
