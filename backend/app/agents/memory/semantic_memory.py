"""Semantic Associative Memory with Vector Similarity Recall."""

import math
from typing import Any, Dict, List, Optional, Tuple
import uuid
from app.agents.memory.base import BaseAgentMemory, MemoryRecord


class SemanticMemory(BaseAgentMemory):
    """Long-term associative vector memory."""

    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.records: List[Tuple[MemoryRecord, List[float]]] = []

    def _embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dimension
        for i, c in enumerate(text.lower()):
            vec[(ord(c) * (i + 1)) % self.dimension] += 1.0
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec

    async def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryRecord:
        rec = MemoryRecord(
            id=str(uuid.uuid4()),
            content=content,
            memory_type="semantic",
            metadata=metadata or {},
        )
        emb = self._embed(content)
        self.records.append((rec, emb))
        return rec

    async def retrieve(self, query: str, top_k: int = 5) -> List[MemoryRecord]:
        q_emb = self._embed(query)
        scored = []
        for rec, emb in self.records:
            dot = sum(a * b for a, b in zip(q_emb, emb))
            scored.append((dot, rec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    async def clear(self) -> None:
        self.records.clear()
