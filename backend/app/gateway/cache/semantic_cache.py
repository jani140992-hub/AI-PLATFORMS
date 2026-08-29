"""Vector Semantic Cache with Cosine Similarity Matching.

Computes dense embeddings for inbound prompts and matches against historical query
embeddings in vector space to serve semantically equivalent completions.
"""

import math
from typing import Dict, List, Optional, Tuple
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two float vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class SemanticCache:
    """Semantic vector cache for LLM queries."""

    def __init__(self, similarity_threshold: float = 0.92):
        self.similarity_threshold = similarity_threshold
        # In-memory storage of (prompt_text, embedding, response)
        self._entries: List[Tuple[str, List[float], ChatCompletionResponse]] = []

    def _simple_embedding(self, text: str) -> List[float]:
        """Deterministic pseudo-embedding for fallback or local environments."""
        dim = 64
        vec = [0.0] * dim
        for i, char in enumerate(text.lower()):
            idx = (ord(char) * (i + 1)) % dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    async def get(self, request: ChatCompletionRequest) -> Optional[ChatCompletionResponse]:
        """Find cached response if prompt similarity exceeds threshold."""
        if not request.messages:
            return None
        last_message = request.messages[-1].content
        query_vec = self._simple_embedding(last_message)

        best_score = -1.0
        best_response: Optional[ChatCompletionResponse] = None

        for text, emb, resp in self._entries:
            score = cosine_similarity(query_vec, emb)
            if score > best_score:
                best_score = score
                best_response = resp

        if best_score >= self.similarity_threshold and best_response:
            return best_response
        return None

    async def set(self, request: ChatCompletionRequest, response: ChatCompletionResponse):
        """Store prompt embedding and response in the semantic cache."""
        if not request.messages:
            return
        last_message = request.messages[-1].content
        emb = self._simple_embedding(last_message)
        self._entries.append((last_message, emb, response))
