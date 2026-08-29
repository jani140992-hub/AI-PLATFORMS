"""Unit Tests for Enterprise RAG, Chunking, BM25, and Hybrid Fusion."""

import pytest
from app.rag.chunkers.recursive_chunker import RecursiveCharacterChunker
from app.rag.search.bm25 import BM25Index
from app.rag.search.hybrid import HybridSearchPipeline


def test_recursive_chunking():
    chunker = RecursiveCharacterChunker(chunk_size=100, chunk_overlap=20)
    text = "Paragraph one with some meaningful sentences.\n\nParagraph two with additional detailed explanation."
    chunks = chunker.chunk(text, "doc-1")
    assert len(chunks) >= 2
    for c in chunks:
        assert len(c.content) <= 120


def test_bm25_lexical_indexing():
    bm25 = BM25Index()
    docs = [
        "Distributed consensus protocols like Raft and Paxos ensure consistency.",
        "Vector databases store dense embeddings for semantic search retrieval.",
        "RAG pipelines combine retrieval with LLM generation.",
    ]
    ids = ["doc_raft", "doc_vector", "doc_rag"]
    bm25.add_documents(ids, docs)

    results = bm25.search("consensus Raft consistency", top_k=1)
    assert len(results) == 1
    assert results[0][0] == "doc_raft"
