"""Sandboxed Python Execution Runner with Safe AST Verification."""

import ast
import contextlib
import io
import sys
from typing import Any, Dict


DISALLOWED_AST_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,
    ast.Global,
    ast.Nonlocal,
)


class SandboxedPythonRunner:
    """Executes safe algorithmic Python code in an isolated scope."""

    @classmethod
    def execute(cls, code_str: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
        # Parse AST and ensure no dangerous primitives exist
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, DISALLOWED_AST_NODES):
                raise PermissionError(f"Disallowed python syntax: {type(node).__name__}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec", "open", "__import__", "compile"):
                    raise PermissionError(f"Disallowed function call: {node.func.id}")

        safe_globals = {
            "__builtins__": {
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "bool": bool,
                "list": list,
                "dict": dict,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "round": round,
                "abs": abs,
                "print": print,
            }
        }
        local_scope: Dict[str, Any] = {}
        stdout_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture):
            compiled = compile(tree, filename="<sandbox>", mode="exec")
            exec(compiled, safe_globals, local_scope)

        return {
            "output": stdout_capture.getvalue(),
            "variables": {k: v for k, v in local_scope.items() if not k.startswith("_")},
        }
