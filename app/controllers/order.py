from app.models import DBCart
from app.repositories import OrderRepository
from core.controller import BaseController


class OrderController(BaseController[DBCart]):
    def __init__(
        self,
        repository: OrderRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: OrderRepository = repository
