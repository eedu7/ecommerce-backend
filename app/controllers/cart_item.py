from app.models import DBCart
from app.repositories import CartItemRepository
from core.controller import BaseController


class CartItemController(BaseController[DBCart]):
    def __init__(
        self,
        repository: CartItemRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: CartItemRepository = repository
