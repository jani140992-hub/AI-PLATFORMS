"""Autonomous Agent Definitions, Memory, and Tool Associations."""

from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin


class AgentDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Autonomous Agent blueprint containing system instructions, tools, and model parameters."""

    __tablename__ = "agents"

    workspace_id: Mapped[str] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    model_provider: Mapped[str] = mapped_column(String(50), default="openai", nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), default="gpt-4o", nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=4096, nullable=False)
    top_p: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), default="vector", nullable=False)  # none, buffer, vector, episodic
    tools_config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="agents")
    sessions: Mapped[List["AgentSession"]] = relationship("AgentSession", back_populates="agent", cascade="all, delete-orphan")


class AgentSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Stateful execution conversation session for an Agent."""

    __tablename__ = "agent_sessions"

    agent_id: Mapped[str] = mapped_column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    session_title: Mapped[str] = mapped_column(String(255), default="New Session", nullable=False)
    context_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    total_tokens_consumed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    agent: Mapped["AgentDefinition"] = relationship("AgentDefinition", back_populates="sessions")
    messages: Mapped[List["SessionMessage"]] = relationship("SessionMessage", back_populates="session", cascade="all, delete-orphan")


class SessionMessage(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Individual message exchange within an Agent Session."""

    __tablename__ = "session_messages"

    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("agent_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # user, assistant, system, tool
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tool_calls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    session: Mapped["AgentSession"] = relationship("AgentSession", back_populates="messages")
