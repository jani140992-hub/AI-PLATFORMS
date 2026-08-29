"""Autonomous Agent Management & Execution Endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import AuthContext, get_auth_context
from app.agents.collaboration.coordinator import MultiAgentCoordinator
from app.agents.collaboration.consensus import ConsensusAgentDeliberation

router = APIRouter()


class AgentRunRequest(BaseModel):
    prompt: str
    mode: str = "coordinator"  # coordinator, consensus


@router.post("/agents/execute")
async def execute_agent_pipeline(
    req: AgentRunRequest,
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Execute multi-agent team or consensus deliberation."""
    if req.mode == "consensus":
        consensus = ConsensusAgentDeliberation()
        return await consensus.run_deliberation(req.prompt)
    else:
        coordinator = MultiAgentCoordinator()
        return await coordinator.execute_task(req.prompt)


@router.get("/agents/archetypes")
async def list_agent_archetypes(auth: AuthContext = Depends(get_auth_context)) -> List[Dict[str, Any]]:
    """List available pre-configured agent archetypes."""
    return [
        {"id": "researcher", "name": "Autonomous Deep Researcher", "tools": ["web_search", "document_search"]},
        {"id": "coder", "name": "Software Engineering Agent", "tools": ["python_runner", "code_linter"]},
        {"id": "analyst", "name": "Financial Data Analyst", "tools": ["calculator", "sql_executor"]},
    ]
