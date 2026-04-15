from app.models import DBCategory, DBSubCategory
from app.repositories import CategoryRepository, SubCategoryRepository
from app.schemas.requests.category import CategoryIn
from core.controller import BaseController


class CategoryController(BaseController[DBCategory]):
    def __init__(
        self,
        category_repository: CategoryRepository,
        sub_category_repository: SubCategoryRepository,
    ) -> None:
        super().__init__(DBCategory, category_repository)
        self.repository: CategoryRepository = category_repository
        self.sub_category_repository: SubCategoryRepository = sub_category_repository

    async def create(
        self,
        data: CategoryIn,
    ) -> DBCategory | DBSubCategory:

        if data.parent_uid is None:
            category = await self.repository.create(data.model_dump(exclude_none=True))
            await self.commit()
            return category

        sub_category = await self.sub_category_repository.create(
            data.model_dump(exclude_none=True)
        )
        await self.commit()
        return sub_category
