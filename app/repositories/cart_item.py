from sqlalchemy import select
from typing import Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBCartItem
from core.repository import BaseRepository


class CartItemRepository(BaseRepository[DBCartItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBCartItem, session)

    async def get_all_by_cart(
        self, cart_uid: UUID, offset: int = 0, limit: int = 20
    ) -> Sequence[DBCartItem]:
        stmt = (
            select(DBCartItem)
            .where(DBCartItem.cart_uid == cart_uid)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_product_uid(self, uid: UUID) -> DBCartItem | None:
        return await self.get_one_by_filters({"product_uid": uid})
