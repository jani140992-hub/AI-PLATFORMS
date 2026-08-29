"""Unit Tests for Multi-Provider AI Gateway & Intelligent Routing."""

import pytest
from app.gateway.manager import gateway_manager
from app.gateway.token_counter import TokenCounter
from app.gateway.circuit_breaker import CircuitBreaker, CircuitState
from app.schemas.gateway import ChatCompletionRequest, ChatMessage


@pytest.mark.asyncio
async def test_token_counter_estimation():
    msg = ChatMessage(role="user", content="Hello world, this is a test prompt for token estimation.")
    toks = TokenCounter.estimate_message_tokens(msg)
    assert toks > 5
    assert toks < 30


@pytest.mark.asyncio
async def test_cost_calculation():
    cost = TokenCounter.calculate_cost("gpt-4o", prompt_tokens=1000, completion_tokens=2000)
    assert cost > 0.0
    assert cost == pytest.approx(0.035, rel=1e-2)


@pytest.mark.asyncio
async def test_circuit_breaker_transitions():
    cb = CircuitBreaker("test-provider", failure_threshold=3, recovery_timeout_seconds=0.1)
    assert cb.allow_request() is True
    assert cb.state == CircuitState.CLOSED

    # Trigger 3 failures
    cb.record_failure()
    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.allow_request() is False


@pytest.mark.asyncio
async def test_gateway_chat_completion_mock():
    req = ChatCompletionRequest(
        model="gpt-4o",
        messages=[ChatMessage(role="user", content="Say test")],
    )
    res = await gateway_manager.execute_chat_completion(req)
    assert res is not None
    assert len(res.choices) > 0
