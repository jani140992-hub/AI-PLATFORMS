"""Ollama Local Model Provider Adapter."""

from app.gateway.providers.openai_provider import OpenAIProvider
from app.core.config import settings


class OllamaProvider(OpenAIProvider):
    """Adapter for locally hosted Ollama instance utilizing OpenAI compatibility layer."""

    def __init__(self, base_url: str | None = None):
        url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/") + "/v1"
        super().__init__(api_key="ollama", base_url=url)
        self.provider_name = "ollama"
        self.default_model = "llama3:latest"

    def is_healthy(self) -> bool:
        return True
