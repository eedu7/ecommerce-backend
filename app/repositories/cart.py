from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import DBCart, DBCartItem
from core.repository import BaseRepository


class CartRepository(BaseRepository[DBCart]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBCart, session)

    async def get_by_user_uid(self, user_uid: UUID) -> DBCart | None:
        stmt = (
            select(DBCart)
            .where(DBCart.user_uid == user_uid)
            .options(selectinload(DBCart.items).selectinload(DBCartItem.product))
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
