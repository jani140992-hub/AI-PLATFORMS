"""Central Tool Discovery and Dispatching Registry."""

from typing import Any, Callable, Dict, List, Optional
from app.agents.tools.base import ToolDefinition, tool
from app.agents.tools.sandbox import SandboxedPythonRunner


# Built-in Standard Tools
@tool("calculator", "Perform arithmetic calculations and evaluate expressions.")
def calculate(expression: str) -> str:
    """Evaluate mathematical expression safely."""
    res = SandboxedPythonRunner.execute(f"result = {expression}")
    return str(res.get("variables", {}).get("result", 0))


@tool("web_search", "Search the internet for up-to-date facts, documentation, or news.")
def web_search(query: str) -> str:
    """Simulated enterprise search tool."""
    return f"[Web Search Results for '{query}']: OmniFlow AI documentation indicates full support for autonomous DAG workflows and hybrid vector search."


@tool("python_runner", "Execute isolated algorithmic Python code safely.")
def run_python(code: str) -> str:
    """Execute Python code in sandbox."""
    res = SandboxedPythonRunner.execute(code)
    return f"STDOUT: {res['output']} | Variables: {res['variables']}"


class ToolRegistry:
    """Registry managing available tools across workspaces."""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {
            "calculator": calculate,
            "web_search": web_search,
            "python_runner": run_python,
        }

    def register(self, tool_def: ToolDefinition) -> None:
        self._tools[tool_def.name] = tool_def

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolDefinition]:
        return list(self._tools.values())

    def get_openai_tool_specs(self) -> List[Dict[str, Any]]:
        return [t.to_openai_schema() for t in self._tools.values()]


tool_registry = ToolRegistry()
