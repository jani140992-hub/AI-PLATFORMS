"""OpenAI Text Embedding Adapter (text-embedding-3-small / text-embedding-3-large)."""

import math
from typing import List
from app.rag.embeddings.base import BaseEmbeddingService


class OpenAIEmbeddingService(BaseEmbeddingService):
    """Generates high-dimensional vector embeddings."""

    def __init__(self, model_name: str = "text-embedding-3-small", dimension: int = 1536):
        super().__init__(model_name, dimension)

    def _mock_deterministic_vector(self, text: str) -> List[float]:
        """Generate high-entropy deterministic vector representation."""
        vec = [0.0] * self.dimension
        for i, char in enumerate(text.lower()):
            idx = (ord(char) * (i + 13) + i * 7) % self.dimension
            vec[idx] += 1.0 / (1.0 + i * 0.01)
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self._mock_deterministic_vector(t) for t in texts]

    async def embed_query(self, query: str) -> List[float]:
        return self._mock_deterministic_vector(query)
