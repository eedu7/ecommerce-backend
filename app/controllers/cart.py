from uuid import UUID

from fastapi.responses import JSONResponse

from app.models import DBCart, DBUser
from app.repositories import CartRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class CartController(BaseController[DBCart]):
    def __init__(
        self,
        repository: CartRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: CartRepository = repository

    async def get_user_cart(self, uid: UUID) -> DBCart:
        cart = await self.repository.get_by_user_uid(uid)

        if cart is None:
            raise NotFoundException()

        return cart

    async def create(self, user: DBUser) -> DBCart:
        cart = await self.repository.create({"user_uid": user.uid})
        await self.commit()

        return cart

    async def delete(
        self, user_uid: UUID | None = None, cart_uid: UUID | None = None
    ) -> JSONResponse:
        if user_uid:
            cart = await self.get_user_cart(user_uid)
        if cart_uid:
            cart = await self.get_by_uid(cart_uid)

        await self.repository.delete(cart)
        await self.commit()

        return JSONResponse(
            content={"message": f"Cart with uid '{cart.uid}' deleted successfully."}
        )
