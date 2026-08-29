"""Common Shared Pydantic Schemas."""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema configured for ORM compatibility."""

    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseModel):
    """Standard pagination query parameters."""

    skip: int = Field(0, ge=0, description="Offset record index")
    limit: int = Field(50, ge=1, le=200, description="Maximum items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""

    total: int
    items: List[T]
    skip: int
    limit: int


class StatusResponse(BaseModel):
    """Generic status acknowledgement response."""

    status: str = "success"
    message: str = "Operation completed successfully"
    details: Optional[dict[str, Any]] = None
