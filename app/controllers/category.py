from app.models import DBCategory
from app.repositories import CategoryRepository
from core.controller import BaseController


class CategoryController(BaseController[DBCategory]):
    def __init__(
        self,
        category_repository: CategoryRepository,
    ) -> None:
        super().__init__(DBCategory, category_repository)
        self.repository: CategoryRepository = category_repository
