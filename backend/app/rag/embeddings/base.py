"""Base Vector Embeddings Generator Interface."""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingService(ABC):
    """Abstract interface for text embedding generation."""

    def __init__(self, model_name: str, dimension: int):
        self.model_name = model_name
        self.dimension = dimension

    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Compute dense vector embeddings for a list of text passages."""
        pass

    @abstractmethod
    async def embed_query(self, query: str) -> List[float]:
        """Compute dense vector embedding for a single search query."""
        pass
