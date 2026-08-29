"""Unit Tests for Graph Multi-Agent State Machine & Execution."""

import pytest
from app.agents.graph.state import GraphState
from app.agents.graph.engine import WorkflowGraph, GraphExecutionEngine
from app.agents.graph.nodes import BaseNode, NodeResult


class MockAddNode(BaseNode):
    def __init__(self, node_id: str, delta: int):
        super().__init__(node_id, f"Add {delta}")
        self.delta = delta

    async def execute(self, state: GraphState) -> NodeResult:
        current = state.get("count", 0)
        return NodeResult(node_id=self.node_id, success=True, output_state_deltas={"count": current + self.delta})


@pytest.mark.asyncio
async def test_graph_state_immutability_and_deltas():
    st = GraphState({"init": 100})
    st.set("key", "val", node_id="node_a")
    assert st.get("key") == "val"
    assert len(st.get_history()) == 1


@pytest.mark.asyncio
async def test_workflow_graph_linear_execution():
    graph = WorkflowGraph("test-wf", "Test Workflow")
    n1 = MockAddNode("step1", 10)
    n2 = MockAddNode("step2", 25)
    graph.add_node(n1)
    graph.add_node(n2)
    graph.set_entry_point("step1")
    graph.add_edge("step1", "step2")
    graph.add_exit_point("step2")

    engine = GraphExecutionEngine(graph)
    final_state = await engine.run({"count": 5})
    assert final_state["count"] == 40
