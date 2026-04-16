from typing import Any, Dict, Generic, Mapping, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import DBBase

T = TypeVar("T", bound=DBBase)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_uid(self, uid: UUID) -> T | None:
        return await self.session.get(self.model, uid)

    async def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[T]:
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_one_by_filters(self, filters: Dict[str, Any]) -> T | None:
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db_in: Dict[str, Any]) -> T:
        db_obj = self.model(**db_in)
        self.session.add(db_obj)
        return db_obj

    async def update(self, db_obj: T, obj_in: Dict[str, Any]) -> T:
        for field, value in obj_in.items():
            if not hasattr(db_obj, field):
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute `{field}`"
                )
            setattr(db_obj, field, value)
        return db_obj

    async def delete(self, db_obj: T) -> None:
        await self.session.delete(db_obj)

    async def flush(self) -> None:
        """Flush the session."""
        await self.session.flush()

    async def refresh(self, db_obj: T) -> None:
        """Refresh the session."""
        await self.session.refresh(db_obj)

    async def commit(self) -> None:
        """Commit the session."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the session."""
        await self.session.rollback()

    def _apply_filters(self, stmt, filters: Mapping[str, Any] | None = None):
        if filters is None:
            return stmt

        for field, value in filters.items():
            column = getattr(self.model, field, None)

            if column is None:
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute '{field}'"
                )
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)
        return stmt
