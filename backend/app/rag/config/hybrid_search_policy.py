"""Hybrid Search and Vector Ingestion Policy.
Configures Reciprocal Rank Fusion (RRF) parameters, neural rerankers, and chunking strategies.
"""

HYBRID_SEARCH_CONFIG = {
    "version": "1.3.0",
    "fusion_algorithm": "reciprocal_rank_fusion",
    "rrf_k_constant": 60,
    "dense_weight": 0.7,
    "sparse_bm25_weight": 0.3,
    "neural_reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "default_top_k": 10,
    "chunking": {
        "chunk_size": 800,
        "chunk_overlap": 150,
        "boundary": "semantic_paragraph",
    },
}
