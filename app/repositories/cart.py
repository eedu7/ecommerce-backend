from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBCart
from core.repository import BaseRepository


class CartRepository(BaseRepository[DBCart]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBCart, session)

    async def get_by_user_uid(self, user_uid: UUID) -> DBCart | None:
        return await self.get_one_by_filters({"user_uid": user_uid})
