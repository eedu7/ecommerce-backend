from fastapi.responses import JSONResponse

from app.models import DBCart, DBUser
from app.repositories import CartRepository
from core.controller import BaseController


class CartController(BaseController[DBCart]):
    def __init__(
        self,
        repository: CartRepository,
    ) -> None:
        super().__init__(DBCart, repository)
        self.repository: CartRepository = repository

    async def create(self, user: DBUser) -> JSONResponse:
        cart = await self.repository.create({"user_uid": user.uid})
        await self.commit()

        return JSONResponse(
            content={
                "message": f"Cart with uid '{cart.uid}' has been created",
                "cart": {"uid": cart.uid},
            }
        )
