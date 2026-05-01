from fastapi import APIRouter, Depends

from core.dependencies.auth import auth_required
from core.dependencies.cart import UserCartDep
from core.dependencies.controller import OrderControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter(dependencies=[Depends(auth_required)])


@router.get("/")
async def get_current_user_orders(
    current_user: CurrentUserDep, controller: OrderControllerDep
):
    return await controller.get_user_orders(current_user.uid)


@router.post("/checkout")
async def checkout(
    controller: OrderControllerDep, user: CurrentUserDep, cart: UserCartDep
):
    return await controller.checkout(user=user, cart=cart)


# TODO: Added the Create Order API Endpoint
# @router.post("/")
# async def create():
#     pass


# TODO: Added the Update Order API Endpoint
# @router.put("/{uid}")
# async def update(uid: UUID):
#     pass


# TODO: Added the Delete Order API Endpoint
# @router.delete("/{uid}")
# async def delete(uid: UUID):
#     pass
