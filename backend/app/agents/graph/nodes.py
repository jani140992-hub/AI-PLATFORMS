"""Graph Node Types and Execution Primitives.

Defines standard node implementations: LLM, Tool Execution, Conditional Branching,
Human-in-the-loop Gateways, and Parallel Fan-Out.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
import time
import uuid

from pydantic import BaseModel, Field
from app.agents.graph.state import GraphState
from app.gateway.manager import gateway_manager
from app.schemas.gateway import ChatCompletionRequest, ChatMessage


class NodeResult(BaseModel):
    """Output artifact produced by executing a graph node."""

    node_id: str
    success: bool = True
    output_state_deltas: Dict[str, Any] = Field(default_factory=dict)
    next_node_override: Optional[str] = None
    pause_for_human_input: bool = False
    tokens_consumed: int = 0
    latency_ms: float = 0.0
    error_message: Optional[str] = None


class BaseNode(ABC):
    """Abstract Base Class for graph nodes."""

    def __init__(self, node_id: str, name: str):
        self.node_id = node_id
        self.name = name

    @abstractmethod
    async def execute(self, state: GraphState) -> NodeResult:
        """Execute node computation against current graph state."""
        pass


class LLMNode(BaseNode):
    """Node invoking an LLM with prompt formatting and state variable injection."""

    def __init__(
        self,
        node_id: str,
        name: str,
        model: str = "gpt-4o",
        system_prompt: str = "You are a helpful AI assistant.",
        user_prompt_template: str = "{input}",
        output_state_key: str = "llm_output",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        super().__init__(node_id, name)
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template
        self.output_state_key = output_state_key
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def execute(self, state: GraphState) -> NodeResult:
        start_time = time.time()
        # Format template with current state values
        current_data = state.snapshot()
        try:
            formatted_prompt = self.user_prompt_template.format(**current_data)
        except KeyError:
            formatted_prompt = self.user_prompt_template

        req = ChatCompletionRequest(
            model=self.model,
            messages=[
                ChatMessage(role="system", content=self.system_prompt),
                ChatMessage(role="user", content=formatted_prompt),
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        try:
            res = await gateway_manager.execute_chat_completion(req)
            content = res.choices[0].message.content
            tokens = res.usage.total_tokens
            latency = (time.time() - start_time) * 1000.0

            return NodeResult(
                node_id=self.node_id,
                success=True,
                output_state_deltas={self.output_state_key: content},
                tokens_consumed=tokens,
                latency_ms=latency,
            )
        except Exception as exc:
            return NodeResult(
                node_id=self.node_id,
                success=False,
                error_message=str(exc),
                latency_ms=(time.time() - start_time) * 1000.0,
            )


class ToolNode(BaseNode):
    """Node executing a registered tool with parameters extracted from state."""

    def __init__(
        self,
        node_id: str,
        name: str,
        tool_func: Callable[..., Any],
        param_mapping: Dict[str, str],
        output_state_key: str = "tool_output",
    ):
        super().__init__(node_id, name)
        self.tool_func = tool_func
        self.param_mapping = param_mapping
        self.output_state_key = output_state_key

    async def execute(self, state: GraphState) -> NodeResult:
        start_time = time.time()
        kwargs = {}
        for param_name, state_key in self.param_mapping.items():
            kwargs[param_name] = state.get(state_key)

        try:
            res = self.tool_func(**kwargs)
            latency = (time.time() - start_time) * 1000.0
            return NodeResult(
                node_id=self.node_id,
                success=True,
                output_state_deltas={self.output_state_key: res},
                latency_ms=latency,
            )
        except Exception as exc:
            return NodeResult(
                node_id=self.node_id,
                success=False,
                error_message=str(exc),
                latency_ms=(time.time() - start_time) * 1000.0,
            )


class ConditionNode(BaseNode):
    """Evaluates conditional logic to select downstream transition edge."""

    def __init__(
        self,
        node_id: str,
        name: str,
        eval_func: Callable[[GraphState], str],
    ):
        super().__init__(node_id, name)
        self.eval_func = eval_func

    async def execute(self, state: GraphState) -> NodeResult:
        start_time = time.time()
        try:
            target_node = self.eval_func(state)
            return NodeResult(
                node_id=self.node_id,
                success=True,
                next_node_override=target_node,
                latency_ms=(time.time() - start_time) * 1000.0,
            )
        except Exception as exc:
            return NodeResult(
                node_id=self.node_id,
                success=False,
                error_message=str(exc),
                latency_ms=(time.time() - start_time) * 1000.0,
            )


class HumanApprovalNode(BaseNode):
    """Pause gate requiring human review before workflow continuation."""

    def __init__(self, node_id: str, name: str, review_message: str):
        super().__init__(node_id, name)
        self.review_message = review_message

    async def execute(self, state: GraphState) -> NodeResult:
        # Pauses execution; resumed via external API approval endpoint
        return NodeResult(
            node_id=self.node_id,
            success=True,
            pause_for_human_input=True,
            output_state_deltas={"approval_pending_message": self.review_message},
        )
