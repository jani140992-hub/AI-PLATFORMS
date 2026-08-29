"""Central AI Gateway Orchestrator.

Orchestrates rate limiting, exact caching, semantic caching, intelligent routing,
circuit breaking, streaming response handling, and usage accounting.
"""

import time
import uuid
from typing import AsyncGenerator, Dict, Any, Optional

from app.gateway.base import StreamChunk, ProviderMetrics
from app.gateway.cache.exact_cache import ExactCache
from app.gateway.cache.semantic_cache import SemanticCache
from app.gateway.circuit_breaker import CircuitBreakerRegistry
from app.gateway.rate_limiter import TokenBucketRateLimiter
from app.gateway.router import LLMRouter
from app.gateway.token_counter import TokenCounter
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse, UsageInfo
from app.core.exceptions import ModelProviderError, RateLimitExceededError


class GatewayManager:
    """Unified Gateway facade for all platform LLM traffic."""

    def __init__(self):
        self.router = LLMRouter()
        self.exact_cache = ExactCache()
        self.semantic_cache = SemanticCache()
        self.rate_limiter = TokenBucketRateLimiter()

    async def execute_chat_completion(
        self, request: ChatCompletionRequest, tenant_id: str = "default"
    ) -> ChatCompletionResponse:
        """Process chat completion through cache -> rate-limit -> routing -> execution -> cache-set."""
        # 1. Rate Limiting Check
        self.rate_limiter.check_limit(tenant_id, tokens_needed=1)

        # 2. Exact Cache Lookup
        cached_exact = await self.exact_cache.get(request)
        if cached_exact:
            return cached_exact

        # 3. Semantic Cache Lookup
        cached_semantic = await self.semantic_cache.get(request)
        if cached_semantic:
            return cached_semantic

        # 4. Resolve Provider and Fallback Chain
        primary_provider = self.router.resolve_provider(request.model)
        provider_chain = self.router.get_healthy_provider_chain(primary_provider.provider_name)

        last_exception = None
        for provider in provider_chain:
            breaker = CircuitBreakerRegistry.get_breaker(provider.provider_name)
            try:
                response = await provider.complete(request)
                breaker.record_success()

                # 5. Populate Caches
                await self.exact_cache.set(request, response)
                await self.semantic_cache.set(request, response)
                return response
            except Exception as exc:
                breaker.record_failure()
                last_exception = exc

        raise ModelProviderError(
            provider="gateway_cluster",
            status_code=502,
            raw_error=f"All upstream providers failed in cascade: {str(last_exception)}",
        )

    async def execute_chat_stream(
        self, request: ChatCompletionRequest, tenant_id: str = "default"
    ) -> AsyncGenerator[StreamChunk, None]:
        """Stream completion tokens via Server-Sent Events."""
        self.rate_limiter.check_limit(tenant_id, tokens_needed=1)
        provider = self.router.resolve_provider(request.model)
        breaker = CircuitBreakerRegistry.get_breaker(provider.provider_name)
        try:
            async for chunk in provider.complete_stream(request):
                yield chunk
            breaker.record_success()
        except Exception as exc:
            breaker.record_failure()
            raise exc


# Singleton Gateway Instance
gateway_manager = GatewayManager()
