from app.models import DBProduct
from app.repositories import ProductRepository
from core.controller import BaseController


class ProductController(BaseController[DBProduct]):
    def __init__(self, repository: ProductRepository) -> None:
        super().__init__(DBProduct, repository)
        self.repository: ProductRepository = repository
