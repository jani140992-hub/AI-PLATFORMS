"""Prompt Registry, Safety Guardrails, and Audit Trail Models."""

from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin


class PromptTemplate(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Versioned Prompt Template stored in the Central Prompt Registry."""

    __tablename__ = "prompt_templates"

    workspace_id: Mapped[str] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="prompts")
    versions: Mapped[List["PromptVersion"]] = relationship("PromptVersion", back_populates="template", cascade="all, delete-orphan")


class PromptVersion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Specific revision of a Prompt Template with input variable schema."""

    __tablename__ = "prompt_versions"

    template_id: Mapped[str] = mapped_column(String(36), ForeignKey("prompt_templates.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    input_variables: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    model_parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    template: Mapped["PromptTemplate"] = relationship("PromptTemplate", back_populates="versions")


class SafetyRule(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Configured moderation or guardrail policy."""

    __tablename__ = "safety_rules"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pii_mask, jailbreak_filter, toxicity, hallucination
    action: Mapped[str] = mapped_column(String(50), default="block", nullable=False)  # block, mask, warn
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AuditLogRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Comprehensive compliance and audit log entry."""

    __tablename__ = "audit_logs"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
