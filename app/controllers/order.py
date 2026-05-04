from uuid import UUID

import stripe
from fastapi.responses import RedirectResponse
from stripe.params import PaymentLinkCreateParams

from app.models import DBCart, DBOrder, DBUser
from app.repositories import (
    CartItemRepository,
    CartRepository,
    OrderItemRepository,
    OrderRepository,
)
from core.config import config
from core.controller import BaseController
from core.exceptions import NotFoundException

stripe.api_key = config.STRIPE_SECRET_KEY

stripe_client = stripe.StripeClient(config.STRIPE_SECRET_KEY)


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

        print("$" * 12)
        print("Cart", cart)
        print("$" * 12)

        order = await self.order_repository.create({"user_uid": user.uid})
        await self.flush()
        await self.refresh(order)

        data: PaymentLinkCreateParams = {
            "line_items": [],
        }

        for item in cart.items:
            await self.order_item_repository.create(
                {
                    "product_uid": item.product_uid,
                    "order_uid": order.uid,
                    "quantity": item.quantity,
                }
            )
            data["line_items"].append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.product.name},
                        "unit_amount": int(item.product.price * 100),
                    },
                    "quantity": item.quantity,
                }
            )

        await self.cart_repository.delete(cart)

        payment_link = stripe_client.payment_links.create(data)

        order.stripe_checkout_session_id = payment_link.id

        await self.commit()

        return {
            "order_uid": order.uid,
            "payment_link": payment_link.url,
        }

        return RedirectResponse(payment_link.url)

    async def get_by_stripe_checkout_session_id(self, session_id: str) -> DBOrder:
        order = await self.order_repository.get_one_by_filters(
            {"stripe_checkout_session_id": session_id}
        )

        if not order:
            raise NotFoundException("Order not found")

        return order
