"""AWS Bedrock Model Provider Adapter."""

import json
import time
import uuid
from typing import AsyncGenerator
from app.gateway.base import BaseLLMProvider, StreamChunk
from app.gateway.token_counter import TokenCounter
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse, ChatChoice, ChatMessage, UsageInfo
from app.core.config import settings
from app.core.exceptions import ModelProviderError


class BedrockProvider(BaseLLMProvider):
    """Adapter for AWS Bedrock Foundation Models."""

    def __init__(self):
        super().__init__(provider_name="bedrock", default_model="anthropic.claude-3-sonnet-20240229-v1:0")
        self.region = settings.BEDROCK_AWS_REGION

    def is_healthy(self) -> bool:
        return True

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        return TokenCounter.calculate_cost(model, prompt_tokens, completion_tokens)

    async def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        # Mock simulated Bedrock invocation for local/hybrid deployment
        prompt_tok = TokenCounter.estimate_prompt_tokens(request.messages)
        comp_tok = 42
        return ChatCompletionResponse(
            id=f"bedrock-{uuid.uuid4()}",
            created=int(time.time()),
            model=request.model or self.default_model,
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(
                        role="assistant",
                        content="[OmniFlow Bedrock Engine]: Processed request via AWS Bedrock.",
                    ),
                    finish_reason="stop",
                )
            ],
            usage=UsageInfo(
                prompt_tokens=prompt_tok,
                completion_tokens=comp_tok,
                total_tokens=prompt_tok + comp_tok,
            ),
        )

    async def complete_stream(
        self, request: ChatCompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        res = await self.complete(request)
        yield StreamChunk(id=res.id, delta_content=res.choices[0].message.content, finish_reason="stop")
