from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import DBProduct
from core.repository import BaseRepository


class ProductRepository(BaseRepository[DBProduct]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBProduct, session)

    async def get_all(self, offset: int = 0, limit: int = 0) -> Sequence[DBProduct]:
        stmt = (
            select(DBProduct)
            .offset(offset)
            .limit(limit)
            .options(selectinload(DBProduct.category))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_uid(self, uid: UUID) -> DBProduct | None:
        stmt = (
            select(DBProduct)
            .where(DBProduct.uid == uid)
            .options(selectinload(DBProduct.category))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> DBProduct | None:
        return await self.get_one_by_filters({"name": name})

    async def get_by_slug(self, slug: str) -> DBProduct | None:
        return await self.get_one_by_filters({"slug": slug})
