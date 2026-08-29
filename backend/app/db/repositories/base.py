"""Generic CRUD Asynchronous Repository Pattern."""

from typing import Any, Generic, List, Optional, Type, TypeVar
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing asynchronous CRUD operations on SQLAlchemy models."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: str) -> Optional[ModelType]:
        """Fetch a single record by primary key."""
        result = await self.session.execute(select(self.model).where(self.model.id == id))  # type: ignore
        return result.scalars().first()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Fetch multiple records with offset and limit pagination."""
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, **kwargs: Any) -> ModelType:
        """Instantiate and persist a new model instance."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: str, **kwargs: Any) -> Optional[ModelType]:
        """Update fields on an existing model instance."""
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(**kwargs)  # type: ignore
        )
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        """Hard delete a record by primary key."""
        result = await self.session.execute(delete(self.model).where(self.model.id == id))  # type: ignore
        return result.rowcount > 0
