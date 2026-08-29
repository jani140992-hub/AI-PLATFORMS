"""AI Gateway Dynamic Routing, Semantic Cache, and Model Catalog Models."""

from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ModelCatalogItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Supported Foundation LLM in the Platform Model Catalog."""

    __tablename__ = "model_catalog"

    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # openai, anthropic, google, deepseek
    model_identifier: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    context_window: Mapped[int] = mapped_column(Integer, default=128000, nullable=False)
    input_cost_per_million: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    output_cost_per_million: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)
    supports_tools: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    supports_vision: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    supports_streaming: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class SemanticCacheEntry(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Cached response keyed by semantic embedding and exact hash."""

    __tablename__ = "semantic_cache_entries"

    prompt_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    model_identifier: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    cached_response: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hit_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
