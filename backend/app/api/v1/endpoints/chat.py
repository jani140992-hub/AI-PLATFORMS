"""OpenAI-Compatible Chat Completions REST and Streaming Endpoints."""

import json
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.api.deps import AuthContext, get_auth_context
from app.gateway.manager import gateway_manager
from app.governance.safety.jailbreak import JailbreakDetector
from app.governance.safety.pii import PIIRedactor
from app.schemas.gateway import ChatCompletionRequest, ChatCompletionResponse
from app.telemetry.metrics import metrics

router = APIRouter()
jailbreak_detector = JailbreakDetector()
pii_redactor = PIIRedactor()


@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    request: ChatCompletionRequest,
    auth: AuthContext = Depends(get_auth_context),
):
    """Unified OpenAI-compatible chat completions endpoint with guardrails and routing."""
    # 1. Safety Guardrails: Prompt Injection Check
    for msg in request.messages:
        jailbreak_detector.enforce(msg.content)
        # Redact PII
        sanitized_content, _ = pii_redactor.redact(msg.content)
        msg.content = sanitized_content

    # 2. Streaming vs Sync
    if request.stream:
        async def event_generator():
            async for chunk in gateway_manager.execute_chat_stream(request, tenant_id=auth.tenant_id):
                chunk_data = {
                    "id": chunk.id,
                    "object": "chat.completion.chunk",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": chunk.delta_content},
                            "finish_reason": chunk.finish_reason,
                        }
                    ],
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # 3. Non-streaming Execution
    res = await gateway_manager.execute_chat_completion(request, tenant_id=auth.tenant_id)
    
    # Record metrics
    metrics.record_token_usage(
        model=request.model,
        prompt_tokens=res.usage.prompt_tokens,
        completion_tokens=res.usage.completion_tokens,
        cost_usd=0.001,
    )
    return res
