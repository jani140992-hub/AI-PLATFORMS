"""Prompt Registry & Template Compiler Endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import AuthContext, get_auth_context
from app.governance.prompts.compiler import PromptCompiler

router = APIRouter()


class PromptCompileRequest(BaseModel):
    template: str
    variables: Dict[str, Any]


@router.post("/prompts/compile")
async def compile_prompt(
    req: PromptCompileRequest,
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Test render a prompt template with variables."""
    compiled = PromptCompiler.compile(req.template, req.variables)
    return compiled.model_dump()
