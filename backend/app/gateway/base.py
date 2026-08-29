"""Abstract Model Provider Interface and Shared Gateway Abstractions.

Defines the contract that all external LLM adapters must fulfill, including
synchronous invocation, asynchronous streaming, tool call normalization,
and cost accounting.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List, Optional
import time

from pydantic import BaseModel, Field
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse, ChatMessage, ChatChoice, UsageInfo


class ProviderMetrics(BaseModel):
    """Execution telemetry captured during provider invocation."""

    provider_name: str
    model_name: str
    request_id: str
    latency_ms: float
    ttft_ms: Optional[float] = None  # Time-to-first-token
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    status_code: int = 200
    is_cached: bool = False
    retry_count: int = 0


class StreamChunk(BaseModel):
    """Standardized normalized token chunk emitted during streaming."""

    id: str
    delta_content: str = ""
    delta_tool_calls: Optional[List[Dict[str, Any]]] = None
    finish_reason: Optional[str] = None
    usage: Optional[UsageInfo] = None


class BaseLLMProvider(ABC):
    """Abstract Base Class for Foundation Model Providers."""

    def __init__(self, provider_name: str, default_model: str, timeout_seconds: float = 60.0):
        self.provider_name = provider_name
        self.default_model = default_model
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    async def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Execute a non-streaming chat completion."""
        pass

    @abstractmethod
    async def complete_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream token chunks asynchronously via Server-Sent Events."""
        pass

    @abstractmethod
    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate the estimated USD cost for a given token consumption."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if provider connection and API keys are verified."""
        pass
