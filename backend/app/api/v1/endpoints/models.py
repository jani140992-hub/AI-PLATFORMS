"""Model Catalog & Status Endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from app.api.deps import AuthContext, get_auth_context

router = APIRouter()


@router.get("/models")
async def list_models(auth: AuthContext = Depends(get_auth_context)) -> Dict[str, Any]:
    """List all available models across registered providers."""
    return {
        "object": "list",
        "data": [
            {"id": "gpt-4o", "provider": "openai", "context_window": 128000, "input_cost_per_m": 5.0, "output_cost_per_m": 15.0},
            {"id": "gpt-4o-mini", "provider": "openai", "context_window": 128000, "input_cost_per_m": 0.15, "output_cost_per_m": 0.60},
            {"id": "claude-3-5-sonnet-20240620", "provider": "anthropic", "context_window": 200000, "input_cost_per_m": 3.0, "output_cost_per_m": 15.0},
            {"id": "gemini-1.5-pro", "provider": "google", "context_window": 1000000, "input_cost_per_m": 3.5, "output_cost_per_m": 10.5},
            {"id": "deepseek-chat", "provider": "deepseek", "context_window": 64000, "input_cost_per_m": 0.14, "output_cost_per_m": 0.28},
            {"id": "meta-llama/Meta-Llama-3-70B-Instruct", "provider": "vllm", "context_window": 8192, "input_cost_per_m": 0.80, "output_cost_per_m": 0.80},
        ]
    }
