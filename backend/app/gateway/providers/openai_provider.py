"""OpenAI Model Provider Adapter."""

import json
import time
import uuid
from typing import AsyncGenerator, Dict, Any, List
import httpx
from app.gateway.base import BaseLLMProvider, StreamChunk
from app.gateway.token_counter import TokenCounter
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse, ChatChoice, ChatMessage, UsageInfo
from app.core.config import settings
from app.core.exceptions import ModelProviderError


class OpenAIProvider(BaseLLMProvider):
    """Production adapter for OpenAI API endpoints."""

    def __init__(self, api_key: str | None = None, base_url: str = "https://api.openai.com/v1"):
        super().__init__(provider_name="openai", default_model="gpt-4o")
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url.rstrip("/")

    def is_healthy(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        return TokenCounter.calculate_cost(model, prompt_tokens, completion_tokens)

    async def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        start_time = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": request.model or self.default_model,
            "messages": [msg.model_dump(exclude_none=True) for msg in request.messages],
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_tokens,
            "stream": False,
        }
        if request.tools:
            payload["tools"] = request.tools
        if request.tool_choice:
            payload["tool_choice"] = request.tool_choice

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                if response.status_code != 200:
                    raise ModelProviderError(
                        provider=self.provider_name,
                        status_code=response.status_code,
                        raw_error=response.text,
                    )
                data = response.json()
                return ChatCompletionResponse(**data)
            except httpx.RequestError as exc:
                raise ModelProviderError(
                    provider=self.provider_name,
                    status_code=503,
                    raw_error=f"Network error: {str(exc)}",
                )

    async def complete_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": request.model or self.default_model,
            "messages": [msg.model_dump(exclude_none=True) for msg in request.messages],
            "temperature": request.temperature,
            "top_p": request.top_p,
            "max_tokens": request.max_tokens,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            async with client.stream(
                "POST", f"{self.base_url}/chat/completions", headers=headers, json=payload
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise ModelProviderError(
                        provider=self.provider_name,
                        status_code=response.status_code,
                        raw_error=error_text.decode("utf-8"),
                    )

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line[6:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk_json = json.loads(data_str)
                        choice = chunk_json["choices"][0]
                        delta = choice.get("delta", {})
                        content = delta.get("content", "")
                        tool_calls = delta.get("tool_calls")
                        finish_reason = choice.get("finish_reason")
                        yield StreamChunk(
                            id=chunk_json.get("id", str(uuid.uuid4())),
                            delta_content=content or "",
                            delta_tool_calls=tool_calls,
                            finish_reason=finish_reason,
                        )
                    except json.JSONDecodeError:
                        continue
