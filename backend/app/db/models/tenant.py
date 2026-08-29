"""Multi-Tenant Organization and Workspace Models."""

from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, SoftDeleteMixin


class Tenant(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Enterprise Tenant entity representing the top-level billing customer."""

    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    plan_tier: Mapped[str] = mapped_column(String(50), default="enterprise", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    monthly_token_quota: Mapped[int] = mapped_column(BigInteger, default=50_000_000, nullable=False)
    tokens_used_this_month: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    billing_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    workspaces: Mapped[List["Workspace"]] = relationship("Workspace", back_populates="tenant", cascade="all, delete-orphan")
    users: Mapped[List["User"]] = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    api_keys: Mapped[List["APIKey"]] = relationship("APIKey", back_populates="tenant", cascade="all, delete-orphan")


class Workspace(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """Isolated project workspace within an Enterprise Tenant."""

    __tablename__ = "workspaces"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="workspaces")
    agents: Mapped[List["AgentDefinition"]] = relationship("AgentDefinition", back_populates="workspace", cascade="all, delete-orphan")
    workflows: Mapped[List["WorkflowDefinition"]] = relationship("WorkflowDefinition", back_populates="workspace", cascade="all, delete-orphan")
    knowledge_bases: Mapped[List["KnowledgeBase"]] = relationship("KnowledgeBase", back_populates="workspace", cascade="all, delete-orphan")
    prompts: Mapped[List["PromptTemplate"]] = relationship("PromptTemplate", back_populates="workspace", cascade="all, delete-orphan")
