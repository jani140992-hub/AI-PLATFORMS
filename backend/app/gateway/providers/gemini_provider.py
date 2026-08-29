"""Google Gemini Model Provider Adapter."""

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


class GoogleGeminiProvider(BaseLLMProvider):
    """Production adapter for Google Gemini 1.5 REST APIs."""

    def __init__(self, api_key: str | None = None):
        super().__init__(provider_name="google", default_model="gemini-1.5-pro")
        self.api_key = api_key or settings.GOOGLE_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def is_healthy(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        return TokenCounter.calculate_cost(model, prompt_tokens, completion_tokens)

    async def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        model = request.model or self.default_model
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"

        contents = []
        system_instruction = None
        for msg in request.messages:
            if msg.role == "system":
                system_instruction = {"parts": [{"text": msg.content}]}
            else:
                role = "user" if msg.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        body: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
                "topP": request.top_p,
            }
        }
        if system_instruction:
            body["systemInstruction"] = system_instruction

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            try:
                response = await client.post(url, json=body)
                if response.status_code != 200:
                    raise ModelProviderError(self.provider_name, response.status_code, response.text)
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                usage = data.get("usageMetadata", {})
                prompt_tok = usage.get("promptTokenCount", 0)
                comp_tok = usage.get("candidatesTokenCount", 0)

                return ChatCompletionResponse(
                    id=f"gemini-{uuid.uuid4()}",
                    created=int(time.time()),
                    model=model,
                    choices=[
                        ChatChoice(
                            index=0,
                            message=ChatMessage(role="assistant", content=text),
                            finish_reason="stop",
                        )
                    ],
                    usage=UsageInfo(
                        prompt_tokens=prompt_tok,
                        completion_tokens=comp_tok,
                        total_tokens=prompt_tok + comp_tok,
                    )
                )
            except Exception as e:
                raise ModelProviderError(self.provider_name, 500, str(e))

    async def complete_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        res = await self.complete(request)
        yield StreamChunk(id=res.id, delta_content=res.choices[0].message.content, finish_reason="stop")
