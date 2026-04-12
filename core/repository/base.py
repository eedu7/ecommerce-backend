from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import DBBase

T = TypeVar("T", bound=DBBase)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_uid(self, uid: UUID) -> T | None:
        return await self.session.get(self.model, uid)

    async def add(self, db_obj: T) -> None:
        self.session.add(db_obj)

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
