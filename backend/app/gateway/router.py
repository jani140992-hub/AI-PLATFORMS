"""Intelligent Dynamic LLM Router and Load Balancer.

Selects optimal model providers according to latency budgets, cost optimization targets,
and circuit breaker availability status.
"""

from typing import Dict, List, Optional
from app.gateway.base import BaseLLMProvider
from app.gateway.circuit_breaker import CircuitBreakerRegistry
from app.gateway.providers.openai_provider import OpenAIProvider
from app.gateway.providers.anthropic_provider import AnthropicProvider
from app.gateway.providers.gemini_provider import GoogleGeminiProvider
from app.gateway.providers.deepseek_provider import DeepSeekProvider
from app.gateway.providers.ollama_provider import OllamaProvider
from app.gateway.providers.vllm_provider import VLLMProvider
from app.gateway.providers.bedrock_provider import BedrockProvider
from app.core.exceptions import ModelProviderError


class LLMRouter:
    """Dynamic multi-provider routing matrix."""

    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleGeminiProvider(),
            "deepseek": DeepSeekProvider(),
            "ollama": OllamaProvider(),
            "vllm": VLLMProvider(),
            "bedrock": BedrockProvider(),
        }
        # Fallback priority cascades
        self.fallback_chains: Dict[str, List[str]] = {
            "openai": ["anthropic", "google", "deepseek", "vllm"],
            "anthropic": ["openai", "google", "deepseek"],
            "google": ["openai", "anthropic"],
            "deepseek": ["openai", "anthropic"],
        }

    def resolve_provider(self, model_or_provider: str) -> BaseLLMProvider:
        """Resolve model name or explicit provider to provider adapter."""
        name = model_or_provider.lower()
        if "gpt" in name or "openai" in name:
            return self.providers["openai"]
        elif "claude" in name or "anthropic" in name:
            return self.providers["anthropic"]
        elif "gemini" in name or "google" in name:
            return self.providers["google"]
        elif "deepseek" in name:
            return self.providers["deepseek"]
        elif "llama" in name or "ollama" in name:
            return self.providers["ollama"]
        return self.providers["openai"]

    def get_healthy_provider_chain(self, primary_provider_name: str) -> List[BaseLLMProvider]:
        """Return healthy provider sequence with circuit breaker checking."""
        chain = [primary_provider_name]
        chain.extend(self.fallback_chains.get(primary_provider_name, ["openai"]))
        
        healthy = []
        for name in chain:
            if name in self.providers:
                breaker = CircuitBreakerRegistry.get_breaker(name)
                if breaker.allow_request():
                    healthy.append(self.providers[name])
        if not healthy:
            # Emergency fallback: return primary provider anyway
            return [self.providers.get(primary_provider_name, self.providers["openai"])]
        return healthy
