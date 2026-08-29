"""SQLAlchemy Declarative Base and Common Model Mixins.

Provides UUID primary keys, timestamp audit fields, soft-delete tracking,
and JSON serialization utilities.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base class for all OmniFlow AI database entities."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert model attributes to a dictionary."""
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns  # type: ignore
        }


class UUIDPrimaryKeyMixin:
    """Mixin for models utilizing UUID version 4 primary keys."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )


class TimestampMixin:
    """Mixin providing created_at and updated_at audit timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin providing soft-deletion lifecycle flag."""

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
