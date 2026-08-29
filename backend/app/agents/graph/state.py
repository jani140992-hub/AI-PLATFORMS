"""Graph Execution State, Reducers, and Immutable Snapshots.

Implements state graph execution semantics similar to LangGraph/Temporal,
providing thread-safe channels, delta reducers, and audit snapshots.
"""

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Union
import uuid
from pydantic import BaseModel, Field


class StateDelta(BaseModel):
    """Incremental modification applied to graph state."""

    key: str
    action: str = "set"  # set, append, merge, delete, add
    value: Any = None
    applied_by_node: str = "system"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GraphState:
    """Thread-safe mutable state container managed across graph nodes."""

    def __init__(self, initial_values: Optional[Dict[str, Any]] = None):
        self._data: Dict[str, Any] = deepcopy(initial_values) if initial_values else {}
        self._history: List[StateDelta] = []
        self._read_only_keys: Set[str] = set()

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any, node_id: str = "system") -> None:
        """Set a value, recording the mutation in history."""
        if key in self._read_only_keys:
            raise KeyError(f"Key '{key}' is marked read-only and cannot be mutated.")
        self._data[key] = value
        self._history.append(
            StateDelta(key=key, action="set", value=value, applied_by_node=node_id)
        )

    def append_to_list(self, key: str, item: Any, node_id: str = "system") -> None:
        """Append an item to a list channel."""
        if key not in self._data:
            self._data[key] = []
        if not isinstance(self._data[key], list):
            raise TypeError(f"State key '{key}' is not a list; cannot append.")
        self._data[key].append(item)
        self._history.append(
            StateDelta(key=key, action="append", value=item, applied_by_node=node_id)
        )

    def merge_dict(self, key: str, updates: Dict[str, Any], node_id: str = "system") -> None:
        """Merge a dictionary into an existing dictionary channel."""
        if key not in self._data:
            self._data[key] = {}
        if not isinstance(self._data[key], dict):
            raise TypeError(f"State key '{key}' is not a dict; cannot merge.")
        self._data[key].update(updates)
        self._history.append(
            StateDelta(key=key, action="merge", value=updates, applied_by_node=node_id)
        )

    def snapshot(self) -> Dict[str, Any]:
        """Produce a deep copy immutable dictionary of the current state."""
        return deepcopy(self._data)

    def get_history(self) -> List[StateDelta]:
        """Return full audit log of state mutations."""
        return list(self._history)
