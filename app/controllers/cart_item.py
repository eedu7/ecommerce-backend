from typing import List
from app.schemas.requests.cart_item import CartItemIn, CartItemUpdateIn
from uuid import UUID
from app.models import DBCartItem
from app.repositories import CartItemRepository
from core.controller import BaseController


class CartItemController(BaseController[DBCartItem]):
    def __init__(
        self,
        repository: CartItemRepository,
    ) -> None:
        super().__init__(DBCartItem, repository)
        self.repository: CartItemRepository = repository

    async def get_all_by_cart(self, cart_uid: UUID, offset: int = 0, limit: int = 20):
        return await self.repository.get_all_by_cart(
            cart_uid=cart_uid, offset=offset, limit=limit
        )

    async def create(self, cart_uid: UUID, data: List[CartItemIn]):
        for item in data:
            await self._add_item(cart_uid, item)

        await self.repository.commit()

        return {"messages": "Cart Item added successfully"}

    async def update(self, uid: UUID, data: CartItemUpdateIn):
        item = await self.get_by_uid(uid)
        item.quantity = data.quantity

        await self.commit()

        return item

    async def delete(self, uid: UUID):
        item = await self.get_by_uid(uid)

        await self.repository.delete(item)
        await self.commit()

        return {"message": f"Cart Item with uid '{uid}' deleted successfully."}

    async def _add_item(self, cart_uid: UUID, item: CartItemIn):

        cart_item = await self.repository.get_by_product_uid(item.product_uid)

        if cart_item:
            cart_item.quantity = item.quantity
        else:
            await self.repository.create({**item.model_dump(), "cart_uid": cart_uid})
