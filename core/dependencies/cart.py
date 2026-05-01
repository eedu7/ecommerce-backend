from typing import Annotated

from fastapi import Depends

from app.models import DBCart
from core.dependencies.controller import CartControllerDep
from core.dependencies.user import CurrentUserDep


async def get_user_cart(
    current_user: CurrentUserDep, controller: CartControllerDep
) -> DBCart:
    return await controller.get_user_cart(current_user.uid)


UserCartDep = Annotated[DBCart, Depends(get_user_cart)]
