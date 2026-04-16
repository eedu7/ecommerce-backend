from typing import Generic, Type, TypeVar
from uuid import UUID

from core.database import DBBase
from core.exceptions import NotFoundException
from core.repository import BaseRepository

T = TypeVar("T", bound=DBBase)


class BaseController(Generic[T]):
    def __init__(self, model: Type[T], repository: BaseRepository) -> None:
        self.model = model
        self.repository = repository

    async def get_by_uid(self, uid: UUID) -> T:
        db_obj = await self.repository.get_by_uid(uid)
        if db_obj is None:
            # TODO: Add a proper message
            raise NotFoundException()
        return db_obj

    async def exists(self, uid: UUID) -> bool:
        db_obj = await self.repository.get_by_uid(uid)
        return db_obj is not None

    async def commit(self) -> None:
        await self.repository.commit()

    async def refresh(self, db_obj: T) -> T:
        await self.repository.refresh(db_obj)
        return db_obj

    async def flush(self) -> None:
        await self.repository.flush()

    async def rollback(self) -> None:
        await self.repository.rollback()
