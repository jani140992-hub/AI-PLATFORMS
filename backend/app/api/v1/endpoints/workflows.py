"""Graph Workflow Creation, Inspection, and Execution Endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid

from app.api.deps import AuthContext, get_auth_context
from app.agents.graph.engine import WorkflowGraph, GraphExecutionEngine
from app.agents.graph.nodes import LLMNode

router = APIRouter()


class WorkflowRunPayload(BaseModel):
    workflow_id: str
    inputs: Dict[str, Any]


@router.post("/workflows/run")
async def trigger_workflow_run(
    payload: WorkflowRunPayload,
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Trigger an execution run of a graph workflow."""
    # Build default pipeline graph
    graph = WorkflowGraph(graph_id=payload.workflow_id, name="Dynamic Execution")
    node1 = LLMNode("step1", "Processor", model="gpt-4o", user_prompt_template="Process: {input}")
    graph.add_node(node1)
    graph.set_entry_point("step1")
    graph.add_exit_point("step1")

    engine = GraphExecutionEngine(graph)
    state = await engine.run(payload.inputs)
    return {
        "run_id": str(uuid.uuid4()),
        "status": "completed",
        "state": state,
    }
