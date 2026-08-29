"""Unified Enterprise Document Ingestion & RAG Query Pipeline."""

from typing import Any, Dict, List, Optional
from app.rag.extractors.pdf_extractor import PDFExtractor
from app.rag.extractors.markdown_extractor import MarkdownExtractor
from app.rag.extractors.code_extractor import CodeExtractor
from app.rag.chunkers.recursive_chunker import RecursiveCharacterChunker
from app.rag.embeddings.openai_embeddings import OpenAIEmbeddingService
from app.rag.search.bm25 import BM25Index
from app.rag.search.hybrid import HybridSearchPipeline, RankedSearchResult
from app.rag.search.reranker import CrossEncoderReranker
from app.rag.stores.qdrant_store import QdrantVectorStore


class RAGPipeline:
    """High-throughput Document Ingestion and Hybrid Vector Query Pipeline."""

    def __init__(self, index_name: str = "default_kb"):
        self.index_name = index_name
        self.pdf_extractor = PDFExtractor()
        self.md_extractor = MarkdownExtractor()
        self.code_extractor = CodeExtractor()
        self.chunker = RecursiveCharacterChunker(chunk_size=800, chunk_overlap=150)
        self.embedding_service = OpenAIEmbeddingService()
        self.vector_store = QdrantVectorStore()
        self.bm25_index = BM25Index()
        self.hybrid_pipeline = HybridSearchPipeline()
        self.reranker = CrossEncoderReranker()
        self._chunks_db: Dict[str, str] = {}

    async def ingest_document(self, file_bytes: bytes, filename: str, doc_id: str) -> int:
        """Extract -> Chunk -> Embed -> Index."""
        # 1. Extraction
        if filename.endswith(".pdf"):
            doc = await self.pdf_extractor.extract(file_bytes, filename)
        elif filename.endswith((".py", ".ts", ".js", ".go", ".rs")):
            doc = await self.code_extractor.extract(file_bytes, filename)
        else:
            doc = await self.md_extractor.extract(file_bytes, filename)

        # 2. Chunking
        chunks = self.chunker.chunk(doc.content, doc_id, metadata={"filename": filename})
        if not chunks:
            return 0

        # 3. Dense Embeddings
        texts = [c.content for c in chunks]
        embeddings = await self.embedding_service.embed_texts(texts)

        # 4. Vector Store Upsert
        chunk_ids = [c.chunk_id for c in chunks]
        payloads = [{"content": c.content, "doc_id": doc_id, "filename": filename} for c in chunks]
        await self.vector_store.upsert_vectors(self.index_name, chunk_ids, embeddings, payloads)

        # 5. BM25 Lexical Index
        self.bm25_index.add_documents(chunk_ids, texts)
        for c in chunks:
            self._chunks_db[c.chunk_id] = c.content

        return len(chunks)

    async def query(self, query_text: str, top_k: int = 5) -> List[RankedSearchResult]:
        """Hybrid Search (Dense + BM25) -> Cross-Encoder Rerank."""
        # Dense Search
        q_emb = await self.embedding_service.embed_query(query_text)
        vector_matches = await self.vector_store.search(self.index_name, q_emb, top_k=top_k * 2)
        dense_results = [
            (vid, score, pay.get("content", ""), pay)
            for vid, score, pay in vector_matches
        ]

        # BM25 Sparse Search
        bm25_results = self.bm25_index.search(query_text, top_k=top_k * 2)

        # Reciprocal Rank Fusion
        fused = self.hybrid_pipeline.reciprocal_rank_fusion(dense_results, bm25_results, top_k=top_k * 2)

        # Neural Cross-Encoder Rerank
        final_reranked = self.reranker.rerank(query_text, fused, top_n=top_k)
        return final_reranked
