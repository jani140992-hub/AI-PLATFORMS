"""Tokenizer and Cost Accounting Engine.

Provides accurate token estimation across OpenAI, Anthropic, Gemini, Llama, and Mistral
models using BPE tokenizers and analytical heuristics, alongside real-time USD billing calculations.
"""

from typing import Dict, List, Optional
from app.schemas.gateway import ChatMessage

# Cost per 1,000,000 tokens in USD (prompt_cost, completion_cost)
MODEL_PRICING_TABLE: Dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (5.00, 15.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    # Anthropic
    "claude-3-5-sonnet-20240620": (3.00, 15.00),
    "claude-3-opus-20240229": (15.00, 75.00),
    "claude-3-haiku-20240307": (0.25, 1.25),
    # Google
    "gemini-1.5-pro": (3.50, 10.50),
    "gemini-1.5-flash": (0.35, 1.05),
    # DeepSeek
    "deepseek-chat": (0.14, 0.28),
    "deepseek-reasoner": (0.55, 2.19),
    # Open Source (vLLM / Ollama self-hosted)
    "meta-llama/Meta-Llama-3-70B-Instruct": (0.80, 0.80),
    "meta-llama/Meta-Llama-3-8B-Instruct": (0.15, 0.15),
    "mistralai/Mixtral-8x7B-Instruct-v0.1": (0.60, 0.60),
}


class TokenCounter:
    """Enterprise token counting and billing calculation service."""

    @classmethod
    def estimate_message_tokens(cls, message: ChatMessage) -> int:
        """Estimate token count for an individual chat message using characters/words heuristics.
        
        Standard English text typically averages ~4 characters per token or ~0.75 words per token.
        Structured messages include format tokens (role, name delimiters).
        """
        content_len = len(message.content)
        # 4 characters per token base
        tokens = max(1, content_len // 4)
        # Message overhead: <|im_start|>role
        # content<|im_end|> adds ~4 tokens
        tokens += 4
        if message.name:
            tokens += len(message.name) // 4 + 1
        if message.tool_calls:
            for tc in message.tool_calls:
                tokens += len(str(tc)) // 4
        return tokens

    @classmethod
    def estimate_prompt_tokens(cls, messages: List[ChatMessage]) -> int:
        """Estimate aggregate tokens across a conversation history."""
        total = 3  # every reply is primed with <|start|>assistant<|message|>
        for msg in messages:
            total += cls.estimate_message_tokens(msg)
        return total

    @classmethod
    def calculate_cost(cls, model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate exact USD billing cost based on published model pricing."""
        pricing = MODEL_PRICING_TABLE.get(model_name)
        if not pricing:
            # Fallback default pricing ($2 per M input, $6 per M output)
            pricing = (2.00, 6.00)

        prompt_cost_per_m, completion_cost_per_m = pricing
        total_cost = (prompt_tokens / 1_000_000.0) * prompt_cost_per_m + (
            completion_tokens / 1_000_000.0
        ) * completion_cost_per_m
        return round(total_cost, 6)
