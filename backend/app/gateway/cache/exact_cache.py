"""Exact SHA-256 Prompt Response Cache."""

import hashlib
import json
from typing import Any, Dict, Optional
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse


class ExactCache:
    """In-memory and Redis exact hash cache."""

    def __init__(self):
        self._memory_store: Dict[str, str] = {}

    def compute_hash(self, request: ChatCompletionRequest) -> str:
        """Generate deterministic hash from messages and generation parameters."""
        data = {
            "model": request.model,
            "temperature": request.temperature,
            "messages": [m.model_dump() for m in request.messages],
        }
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    async def get(self, request: ChatCompletionRequest) -> Optional[ChatCompletionResponse]:
        key = self.compute_hash(request)
        cached_json = self._memory_store.get(key)
        if cached_json:
            return ChatCompletionResponse.model_validate_json(cached_json)
        return None

    async def set(self, request: ChatCompletionRequest, response: ChatCompletionResponse, ttl_seconds: int = 3600):
        key = self.compute_hash(request)
        self._memory_store[key] = response.model_dump_json()
