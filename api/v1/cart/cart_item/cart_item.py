from core.dependencies.cart import UserCartDep
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.requests.cart_item import CartItemIn, CartItemUpdateIn
from core.dependencies.auth import auth_required
from core.dependencies.controller import CartItemControllerDep

router = APIRouter(dependencies=[Depends(auth_required)])


@router.get("/items")
async def get(
    cart: UserCartDep,
    controller: CartItemControllerDep,
    offset: int = 0,
    limit: int = 20,
):
    return await controller.get_all_by_cart(cart.uid, offset=offset, limit=limit)


@router.post("/items")
async def create(
    cart: UserCartDep,
    data: List[CartItemIn],
    controller: CartItemControllerDep,
):
    return await controller.create(cart.uid, data)


@router.put("/items/{item_uid}")
async def update(
    item_uid: UUID,
    data: CartItemUpdateIn,
    controller: CartItemControllerDep,
):
    return await controller.update(item_uid, data)


@router.delete("/items/{item_uid}")
async def delete(
    item_uid: UUID,
    controller: CartItemControllerDep,
):
    return await controller.delete(item_uid)
