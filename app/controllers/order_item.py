from app.models import DBCart
from app.repositories import OrderItemRepository
from core.controller import BaseController


class OrderItemController(BaseController[DBCart]):
    def __init__(
        self,
        repository: OrderItemRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: OrderItemRepository = repository
