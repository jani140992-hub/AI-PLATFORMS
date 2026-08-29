"""High-Throughput vLLM Provider Adapter."""

from app.gateway.providers.openai_provider import OpenAIProvider
from app.core.config import settings


class VLLMProvider(OpenAIProvider):
    """Adapter for high-performance vLLM cluster endpoints."""

    def __init__(self, base_url: str | None = None):
        url = (base_url or settings.VLLM_BASE_URL or "http://localhost:8000").rstrip("/") + "/v1"
        super().__init__(api_key="vllm-token", base_url=url)
        self.provider_name = "vllm"
        self.default_model = "meta-llama/Meta-Llama-3-70B-Instruct"
