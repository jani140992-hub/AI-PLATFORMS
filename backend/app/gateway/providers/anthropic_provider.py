"""Anthropic Claude Provider Adapter."""

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


class AnthropicProvider(BaseLLMProvider):
    """Production adapter for Anthropic Claude Messages API."""

    def __init__(self, api_key: str | None = None, base_url: str = "https://api.anthropic.com/v1"):
        super().__init__(provider_name="anthropic", default_model="claude-3-5-sonnet-20240620")
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.base_url = base_url.rstrip("/")

    def is_healthy(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        return TokenCounter.calculate_cost(model, prompt_tokens, completion_tokens)

    def _convert_messages(self, messages: List[ChatMessage]) -> tuple[Optional[str], List[Dict[str, str]]]:
        system_prompt = None
        anthropic_msgs = []
        for msg in messages:
            if msg.role == "system":
                system_prompt = msg.content
            else:
                anthropic_msgs.append({
                    "role": "assistant" if msg.role == "assistant" else "user",
                    "content": msg.content,
                })
        return system_prompt, anthropic_msgs

    async def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        system_prompt, formatted_messages = self._convert_messages(request.messages)
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": request.model or self.default_model,
            "messages": formatted_messages,
            "max_tokens": request.max_tokens or 4096,
            "temperature": request.temperature,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/messages",
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
                content_text = ""
                for part in data.get("content", []):
                    if part.get("type") == "text":
                        content_text += part.get("text", "")

                prompt_tokens = data.get("usage", {}).get("input_tokens", 0)
                completion_tokens = data.get("usage", {}).get("output_tokens", 0)

                return ChatCompletionResponse(
                    id=data.get("id", str(uuid.uuid4())),
                    created=int(time.time()),
                    model=request.model,
                    choices=[
                        ChatChoice(
                            index=0,
                            message=ChatMessage(role="assistant", content=content_text),
                            finish_reason="stop",
                        )
                    ],
                    usage=UsageInfo(
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        total_tokens=prompt_tokens + completion_tokens,
                    ),
                )
            except httpx.RequestError as exc:
                raise ModelProviderError(
                    provider=self.provider_name,
                    status_code=503,
                    raw_error=f"Network error: {str(exc)}",
                )

    async def complete_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        system_prompt, formatted_messages = self._convert_messages(request.messages)
        headers = {
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": request.model or self.default_model,
            "messages": formatted_messages,
            "max_tokens": request.max_tokens or 4096,
            "temperature": request.temperature,
            "stream": True,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            async with client.stream("POST", f"{self.base_url}/messages", headers=headers, json=payload) as response:
                if response.status_code != 200:
                    err = await response.aread()
                    raise ModelProviderError(self.provider_name, response.status_code, err.decode())

                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    raw = line[6:].strip()
                    try:
                        event = json.loads(raw)
                        event_type = event.get("type")
                        if event_type == "content_block_delta":
                            delta = event.get("delta", {})
                            if delta.get("type") == "text_delta":
                                yield StreamChunk(
                                    id=str(uuid.uuid4()),
                                    delta_content=delta.get("text", ""),
                                )
                        elif event_type == "message_stop":
                            yield StreamChunk(id=str(uuid.uuid4()), finish_reason="stop")
                            break
                    except json.JSONDecodeError:
                        continue
