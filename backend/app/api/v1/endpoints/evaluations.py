"""Evaluation Benchmarks & LLM-as-a-Judge Endpoints."""

from typing import Any, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import AuthContext, get_auth_context
from app.governance.evaluations.benchmarks import BenchmarkSuite
from app.governance.evaluations.rag_triad import RAGTriadEvaluator

router = APIRouter()


class RAGTriadRequest(BaseModel):
    query: str
    context: list[str]
    answer: str


@router.post("/evaluations/benchmarks/mmlu")
async def run_mmlu_benchmark(
    model: str = "gpt-4o",
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Execute MMLU benchmark against model."""
    result = await BenchmarkSuite.evaluate_mmlu(model)
    return result.model_dump()


@router.post("/evaluations/rag-triad")
async def evaluate_rag_triad(
    req: RAGTriadRequest,
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Compute Context Relevance, Groundedness, and Answer Relevance."""
    evaluator = RAGTriadEvaluator()
    score = await evaluator.evaluate(req.query, req.context, req.answer)
    return score.model_dump()
