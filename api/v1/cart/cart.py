from uuid import UUID

from fastapi import APIRouter, Depends

from core.dependencies.auth import auth_required
from core.dependencies.controller import CartControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter(dependencies=[Depends(auth_required)])


@router.get("/")
async def get_carts(controller: CartControllerDep):
    return await controller.get_all()


@router.get("/me")
async def get_user_cart(user: CurrentUserDep, controller: CartControllerDep):
    return await controller.get_user_cart(user.uid)


@router.get("/{uid}")
async def get_cart(uid: UUID, controller: CartControllerDep):
    return await controller.get_by_uid(uid)


@router.post("/")
async def create(user: CurrentUserDep, controller: CartControllerDep):
    return await controller.create(user)


@router.delete("/{uid}")
async def delete(uid: UUID, controller: CartControllerDep):
    return await controller.delete(cart_uid=uid)


@router.delete("/")
async def delete_user_cart(user: CurrentUserDep, controller: CartControllerDep):
    return await controller.delete(user_uid=user.uid)
