"""Graph-Based Multi-Agent Workflow Engine Models."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin


class WorkflowDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """DAG/Graph Workflow definition containing nodes and edges."""

    __tablename__ = "workflows"

    workspace_id: Mapped[str] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    graph_schema: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # Nodes, Edges, Configurations
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="workflows")
    runs: Mapped[List["WorkflowRun"]] = relationship("WorkflowRun", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowRun(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Instance execution run of a Workflow graph."""

    __tablename__ = "workflow_runs"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)  # pending, running, completed, failed, paused
    input_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    output_payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    workflow: Mapped["WorkflowDefinition"] = relationship("WorkflowDefinition", back_populates="runs")
    step_executions: Mapped[List["WorkflowStepExecution"]] = relationship("WorkflowStepExecution", back_populates="run", cascade="all, delete-orphan")


class WorkflowStepExecution(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Execution step log of an individual node in the graph."""

    __tablename__ = "workflow_step_executions"

    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    node_name: Mapped[str] = mapped_column(String(255), nullable=False)
    node_type: Mapped[str] = mapped_column(String(50), nullable=False)  # llm, tool, condition, human_approval, router
    status: Mapped[str] = mapped_column(String(50), default="running", nullable=False)
    input_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    output_state: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    tokens_consumed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="step_executions")
