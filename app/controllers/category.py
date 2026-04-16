from slugify.slugify import slugify

from app.models import DBCategory
from app.repositories import CategoryRepository
from app.schemas.requests.category import CategoryIn
from core.controller import BaseController


class CategoryController(BaseController[DBCategory]):
    def __init__(
        self,
        category_repository: CategoryRepository,
    ) -> None:
        super().__init__(DBCategory, category_repository)
        self.repository: CategoryRepository = category_repository

    async def create(self, data: CategoryIn) -> DBCategory:
        db_obj = await self.repository.create(
            {**data.model_dump(), "slug": slugify(data.name)}
        )
        await self.commit()
        return db_obj
