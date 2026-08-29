"""Tool Definition Decorators and Parameter Schemas."""

import inspect
from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel, create_model


class ToolParameter(BaseModel):
    """Metadata for tool arguments."""

    name: str
    type_name: str
    description: str
    required: bool = True


class ToolDefinition:
    """Registered tool specification available for agent dispatch."""

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[..., Any],
        parameters: Dict[str, Any],
    ):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert tool signature to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters.get("properties", {}),
                    "required": self.parameters.get("required", []),
                },
            },
        }


def tool(name: str, description: str) -> Callable[[Callable[..., Any]], ToolDefinition]:
    """Decorator to register a python function as an agent tool."""
    def decorator(fn: Callable[..., Any]) -> ToolDefinition:
        sig = inspect.signature(fn)
        props = {}
        required = []
        for param_name, param in sig.parameters.items():
            props[param_name] = {"type": "string", "description": f"Parameter {param_name}"}
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return ToolDefinition(
            name=name,
            description=description,
            func=fn,
            parameters={"properties": props, "required": required},
        )
    return decorator
