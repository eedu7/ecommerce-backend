from uuid import UUID

from fastapi import APIRouter

from core.dependencies.controller import OrderItemControllerDep

router = APIRouter()


@router.get("/{order_uid}/items")
async def get(order_uid: UUID, controller: OrderItemControllerDep):
    pass


@router.post("/{order_uid}/items")
async def create(order_uid: UUID, controller: OrderItemControllerDep):
    pass


@router.put("/{order_uid}/items/{item_uid}")
async def update(order_uid: UUID, item_uid: UUID, controller: OrderItemControllerDep):
    pass


@router.delete("/{order_uid}/items/{item_uid}")
async def delete(order_uid: UUID, item_uid: UUID, controller: OrderItemControllerDep):
    pass
