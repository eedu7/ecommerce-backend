from app.models import DBCategory
from app.repositories import CategoryRepository, SubCategoryRepository
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
