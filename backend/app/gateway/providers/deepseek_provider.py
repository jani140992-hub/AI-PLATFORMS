"""DeepSeek V3 / R1 Provider Adapter."""

from app.gateway.providers.openai_provider import OpenAIProvider
from app.core.config import settings


class DeepSeekProvider(OpenAIProvider):
    """Adapter for DeepSeek AI platform utilizing OpenAI-compatible API interface."""

    def __init__(self, api_key: str | None = None):
        super().__init__(
            api_key=api_key or settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1",
        )
        self.provider_name = "deepseek"
        self.default_model = "deepseek-chat"
