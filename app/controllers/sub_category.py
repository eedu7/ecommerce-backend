from slugify import slugify

from app.models import DBSubCategory
from app.repositories import SubCategoryRepository
from app.schemas.requests.sub_category import SubCategoryIn
from core.controller import BaseController


class SubCategoryController(BaseController[DBSubCategory]):
    def __init__(
        self,
        repository: SubCategoryRepository,
    ) -> None:
        super().__init__(DBSubCategory, repository)
        self.repository: SubCategoryRepository = repository

    async def create(self, data: SubCategoryIn) -> DBSubCategory:

        db_obj = await self.repository.create(
            {
                "name": data.name,
                "category_uid": data.category_uid,
                "slug": slugify(data.name),
            }
        )
        await self.commit()
        return db_obj
