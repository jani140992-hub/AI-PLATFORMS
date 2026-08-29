"""Graph Execution Engine & DAG Runtime.

Manages topological sorting, cyclical state iteration limits, breakpoint triggers,
and asynchronous step dispatching.
"""

import asyncio
from typing import Callable, Dict, List, Optional, Set
import time

from app.agents.graph.nodes import BaseNode, NodeResult
from app.agents.graph.state import GraphState
from app.core.exceptions import InvalidWorkflowGraphError, WorkflowExecutionError


class Edge:
    """Directed connection between two nodes."""

    def __init__(self, source_id: str, target_id: str, condition: Optional[Callable[[GraphState], bool]] = None):
        self.source_id = source_id
        self.target_id = target_id
        self.condition = condition


class WorkflowGraph:
    """Directed Graph of executable nodes and conditional edges."""

    def __init__(self, graph_id: str, name: str, max_iterations: int = 50):
        self.graph_id = graph_id
        self.name = name
        self.max_iterations = max_iterations
        self.nodes: Dict[str, BaseNode] = {}
        self.edges: List[Edge] = []
        self.entry_point: Optional[str] = None
        self.exit_points: Set[str] = set()

    def add_node(self, node: BaseNode) -> None:
        self.nodes[node.node_id] = node

    def set_entry_point(self, node_id: str) -> None:
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' not found in graph.")
        self.entry_point = node_id

    def add_edge(self, source_id: str, target_id: str, condition: Optional[Callable[[GraphState], bool]] = None) -> None:
        if source_id not in self.nodes or target_id not in self.nodes:
            raise KeyError("Both source and target nodes must exist in graph before adding edge.")
        self.edges.append(Edge(source_id, target_id, condition))

    def add_exit_point(self, node_id: str) -> None:
        self.exit_points.add(node_id)


class GraphExecutionEngine:
    """Runtime orchestrator executing graph workflows with checkpointing."""

    def __init__(self, graph: WorkflowGraph):
        self.graph = graph

    async def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute graph from entry point until an exit point or iteration cap."""
        if not self.graph.entry_point:
            raise InvalidWorkflowGraphError("Graph has no designated entry point.", violations=["missing_entry_point"])

        state = GraphState(initial_state)
        current_node_id: Optional[str] = self.graph.entry_point
        iteration_count = 0
        total_tokens = 0

        while current_node_id and iteration_count < self.graph.max_iterations:
            iteration_count += 1
            node = self.graph.nodes.get(current_node_id)
            if not node:
                raise WorkflowExecutionError(self.graph.graph_id, current_node_id, "Target node missing.")

            # Execute node
            result: NodeResult = await node.execute(state)
            total_tokens += result.tokens_consumed

            if not result.success:
                raise WorkflowExecutionError(
                    self.graph.graph_id, current_node_id, result.error_message or "Node execution failed."
                )

            # Apply state mutations
            for k, v in result.output_state_deltas.items():
                state.set(k, v, node_id=current_node_id)

            if result.pause_for_human_input:
                state.set("_status", "paused_for_approval")
                break

            if current_node_id in self.graph.exit_points:
                break

            # Resolve next node
            if result.next_node_override:
                current_node_id = result.next_node_override
            else:
                # Find matching outgoing edge
                next_candidates = [e for e in self.graph.edges if e.source_id == current_node_id]
                next_target = None
                for edge in next_candidates:
                    if edge.condition is None or edge.condition(state):
                        next_target = edge.target_id
                        break
                current_node_id = next_target

        state.set("_total_iterations", iteration_count)
        state.set("_total_tokens_consumed", total_tokens)
        return state.snapshot()
