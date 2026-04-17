from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBProduct
from core.repository import BaseRepository


class ProductRepository(BaseRepository[DBProduct]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBProduct, session)

    async def get_by_name(self, name: str) -> DBProduct | None:
        return await self.get_one_by_filters({"name": name})

    async def get_by_slug(self, slug: str) -> DBProduct | None:
        return await self.get_one_by_filters({"slug": slug})
