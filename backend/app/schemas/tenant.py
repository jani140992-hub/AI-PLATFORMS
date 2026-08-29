"""Tenant and Workspace Pydantic Schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import BaseSchema


class TenantCreate(BaseModel):
    """Schema for registering a new Enterprise Tenant."""

    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=100)
    billing_email: Optional[EmailStr] = None
    monthly_token_quota: int = Field(50_000_000, ge=1_000_000)


class TenantRead(BaseSchema):
    """Schema for returning Tenant details."""

    id: str
    name: str
    slug: str
    plan_tier: str
    is_active: bool
    monthly_token_quota: int
    tokens_used_this_month: int
    billing_email: Optional[str] = None
    created_at: datetime


class WorkspaceCreate(BaseModel):
    """Schema for creating an isolated Workspace."""

    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class WorkspaceRead(BaseSchema):
    """Schema for returning Workspace details."""

    id: str
    tenant_id: str
    name: str
    slug: str
    description: Optional[str]
    is_default: bool
    created_at: datetime
