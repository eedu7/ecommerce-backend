from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBSubCategory
from core.repository import BaseRepository


class SubCategoryRepository(BaseRepository[DBSubCategory]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBSubCategory, session)

    async def get_by_name(self, name: str) -> DBSubCategory | None:
        return await self.get_one_by_filters({"name": name})

    async def get_by_slug(self, slug: str) -> DBSubCategory | None:
        return await self.get_one_by_filters({"slug": slug})
