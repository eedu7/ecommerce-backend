from app.models import DBCart
from app.repositories import CartRepository
from core.controller import BaseController


class CartController(BaseController[DBCart]):
    def __init__(
        self,
        repository: CartRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: CartRepository = repository
