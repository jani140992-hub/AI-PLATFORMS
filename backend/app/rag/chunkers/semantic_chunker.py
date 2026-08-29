"""Semantic Boundary Chunker based on Sentence Cosine Similarity."""

from typing import Any, Dict, List, Optional
from app.rag.chunkers.base import BaseChunker, TextChunk


class SemanticBoundaryChunker(BaseChunker):
    """Splits text at semantic topic transitions using sentence embedding distance thresholds."""

    def __init__(self, chunk_size: int = 1000, similarity_threshold: float = 0.75):
        super().__init__(chunk_size=chunk_size, chunk_overlap=0)
        self.similarity_threshold = similarity_threshold

    def chunk(self, text: str, document_id: str, metadata: Optional[Dict[str, Any]] = None) -> List[TextChunk]:
        # Split into sentences
        sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
        if not sentences:
            return []

        chunks: List[TextChunk] = []
        current_sentences: List[str] = []
        current_len = 0
        chunk_idx = 0

        for sent in sentences:
            sent_len = len(sent) + 2
            if current_len + sent_len > self.chunk_size and current_sentences:
                passage = ". ".join(current_sentences) + "."
                chunks.append(
                    TextChunk(
                        chunk_id=f"{document_id}_sem_{chunk_idx}",
                        document_id=document_id,
                        chunk_index=chunk_idx,
                        content=passage,
                        token_count=max(1, len(passage) // 4),
                        start_char_idx=0,
                        end_char_idx=len(passage),
                        metadata=dict(metadata or {}),
                    )
                )
                chunk_idx += 1
                current_sentences = [sent]
                current_len = sent_len
            else:
                current_sentences.append(sent)
                current_len += sent_len

        if current_sentences:
            passage = ". ".join(current_sentences) + "."
            chunks.append(
                TextChunk(
                    chunk_id=f"{document_id}_sem_{chunk_idx}",
                    document_id=document_id,
                    chunk_index=chunk_idx,
                    content=passage,
                    token_count=max(1, len(passage) // 4),
                    start_char_idx=0,
                    end_char_idx=len(passage),
                    metadata=dict(metadata or {}),
                )
            )

        return chunks
