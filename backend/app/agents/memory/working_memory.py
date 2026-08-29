"""Working Memory Buffer with FIFO Windowing and Token Budget Limits."""

from typing import Any, Dict, List, Optional
import uuid
from app.agents.memory.base import BaseAgentMemory, MemoryRecord


class WorkingMemory(BaseAgentMemory):
    """Sliding-window short-term conversational scratchpad memory."""

    def __init__(self, max_records: int = 15):
        self.max_records = max_records
        self.records: List[MemoryRecord] = []

    async def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> MemoryRecord:
        rec = MemoryRecord(
            id=str(uuid.uuid4()),
            content=content,
            memory_type="working",
            metadata=metadata or {},
        )
        self.records.append(rec)
        if len(self.records) > self.max_records:
            self.records.pop(0)  # Evict oldest record
        return rec

    async def retrieve(self, query: str, top_k: int = 5) -> List[MemoryRecord]:
        # Working memory returns the most recent items
        return self.records[-top_k:]

    async def clear(self) -> None:
        self.records.clear()
