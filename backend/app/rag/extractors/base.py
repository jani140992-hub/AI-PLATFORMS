"""Base Document Extractor Interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ExtractedDocument(BaseModel):
    """Raw parsed content and metadata extracted from source documents."""

    source_id: str
    filename: str
    content: str
    content_type: str
    file_size_bytes: int
    page_count: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseExtractor(ABC):
    """Abstract Base Class for file format extractors."""

    @abstractmethod
    async def extract(self, file_bytes: bytes, filename: str, **kwargs: Any) -> ExtractedDocument:
        """Parse raw file bytes into standard ExtractedDocument format."""
        pass
