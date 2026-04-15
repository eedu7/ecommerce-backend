from app.models import DBSubCategory
from app.repositories import SubCategoryRepository
from core.controller import BaseController


class SubCategoryController(BaseController[DBSubCategory]):
    def __init__(
        self,
        repository: SubCategoryRepository,
    ) -> None:
        super().__init__(DBSubCategory, repository)
        self.repository: SubCategoryRepository = repository
