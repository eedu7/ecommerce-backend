from uuid import UUID

from app.models import DBCart, DBOrder, DBUser
from app.repositories import (
    CartItemRepository,
    CartRepository,
    OrderItemRepository,
    OrderRepository,
)
from core.controller import BaseController


class OrderController(BaseController[DBOrder]):
    def __init__(
        self,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
    ) -> None:
        super().__init__(DBOrder, order_repository)
        self.order_repository: OrderRepository = order_repository
        self.order_item_repository: OrderItemRepository = order_item_repository
        self.cart_repository: CartRepository = cart_repository
        self.cart_item_repository: CartItemRepository = cart_item_repository

    async def get_user_orders(self, user_uid: UUID):
        return await self.order_repository.get_by_user_uid(user_uid)

    async def checkout(self, user: DBUser, cart: DBCart):

        order = await self.order_repository.create({"user_uid": user.uid})
        await self.flush()
        await self.refresh(order)

        for item in cart.items:
            await self.order_item_repository.create(
                {
                    "product_uid": item.product_uid,
                    "order_uid": order.uid,
                    "quantity": item.quantity,
                }
            )

        await self.cart_repository.delete(cart)

        await self.commit()
        return {"message": "Checkout success"}
