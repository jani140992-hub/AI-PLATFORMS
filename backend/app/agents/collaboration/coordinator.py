"""Hierarchical Supervisor-Worker Multi-Agent Pattern."""

from typing import Any, Dict, List
from app.agents.graph.engine import WorkflowGraph, GraphExecutionEngine
from app.agents.graph.nodes import LLMNode, BaseNode, NodeResult
from app.agents.graph.state import GraphState


class MultiAgentCoordinator:
    """Orchestrates decomposition of complex tasks across specialized agents."""

    def __init__(self, supervisor_model: str = "gpt-4o", worker_model: str = "gpt-4o-mini"):
        self.supervisor_model = supervisor_model
        self.worker_model = worker_model

    def build_team_graph(self, task_name: str) -> WorkflowGraph:
        """Construct a 3-agent pipeline: Planner -> Specialist Worker -> Quality Reviewer."""
        graph = WorkflowGraph(graph_id=f"team-{task_name}", name=f"Team {task_name}")

        planner = LLMNode(
            node_id="planner",
            name="Task Planner",
            model=self.supervisor_model,
            system_prompt="You are a Chief AI Architect. Break down the user prompt into structured actionable subtasks.",
            user_prompt_template="Plan the following task: {input}",
            output_state_key="plan",
        )

        worker = LLMNode(
            node_id="worker",
            name="Specialist Worker",
            model=self.worker_model,
            system_prompt="You are an expert software engineer. Execute the provided plan comprehensively.",
            user_prompt_template="Execute this plan: {plan}\nOriginal user input: {input}",
            output_state_key="draft_solution",
        )

        reviewer = LLMNode(
            node_id="reviewer",
            name="Quality Reviewer",
            model=self.supervisor_model,
            system_prompt="You are a principal QA engineer. Audit the draft solution for accuracy, edge cases, and robustness.",
            user_prompt_template="Review this solution:\n{draft_solution}\nAgainst the plan:\n{plan}",
            output_state_key="final_output",
        )

        graph.add_node(planner)
        graph.add_node(worker)
        graph.add_node(reviewer)

        graph.set_entry_point("planner")
        graph.add_edge("planner", "worker")
        graph.add_edge("worker", "reviewer")
        graph.add_exit_point("reviewer")

        return graph

    async def execute_task(self, task_prompt: str) -> Dict[str, Any]:
        graph = self.build_team_graph("dynamic_task")
        engine = GraphExecutionEngine(graph)
        return await engine.run({"input": task_prompt})
