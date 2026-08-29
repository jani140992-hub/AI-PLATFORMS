"""Base Text Chunker Interface and Chunk Model."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    """Discrete passage chunk extracted from document."""

    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    token_count: int
    start_char_idx: int
    end_char_idx: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseChunker(ABC):
    """Abstract Base Class for text chunkers."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def chunk(self, text: str, document_id: str, metadata: Optional[Dict[str, Any]] = None) -> List[TextChunk]:
        """Divide source text into chunks."""
        pass
