from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.requests.cart_item import CartItemIn
from core.dependencies.auth import auth_required
from core.dependencies.controller import CartItemControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter(
    dependencies=[Depends(auth_required)]
)


@router.get("/{cart_uid}/items")
async def get(cart_uid: UUID, user: CurrentUserDep, controller: CartItemControllerDep):
    pass


@router.post("/{cart_uid}/items")
async def create(
    cart_uid: UUID,
    data: CartItemIn,
    user: CurrentUserDep,
    controller: CartItemControllerDep,
):
    pass


@router.put("/{cart_uid}/items/{item_uid}")
async def update(
    cart_uid: UUID,
    item_uid: UUID,
    user: CurrentUserDep,
    controller: CartItemControllerDep,
):
    pass


@router.delete("/{cart_uid}/items/{item_uid}")
async def delete(
    cart_uid: UUID,
    item_uid: UUID,
    user: CurrentUserDep,
    controller: CartItemControllerDep,
):
    pass
