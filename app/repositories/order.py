from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBOrder
from core.repository import BaseRepository


class OrderRepository(BaseRepository[DBOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBOrder, session)

    async def get_by_user_uid(self, user_uid: UUID) -> Sequence[DBOrder]:
        stmt = select(DBOrder).where(DBOrder.user_uid == user_uid)
        result = await self.session.execute(stmt)
        return result.scalars().all()
