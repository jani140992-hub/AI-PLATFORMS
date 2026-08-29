"""Base Memory Abstraction for Autonomous Agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    """Unit memory trace stored in agent memory systems."""

    id: str
    content: str
    memory_type: str = "semantic"
    importance_score: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgentMemory(ABC):
    """Abstract Memory Interface."""

    @abstractmethod
    async def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryRecord:
        """Store a new memory item."""
        pass

    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 5) -> List[MemoryRecord]:
        """Recall top relevant memories based on query."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Flush memory store."""
        pass
