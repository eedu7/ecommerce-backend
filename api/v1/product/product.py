from uuid import UUID

from fastapi import APIRouter

from app.schemas.requests.product import ProductIn, ProductUpdateIn
from core.dependencies.controller import ProductControllerDep

router = APIRouter()


@router.get("/")
async def get_all(controller: ProductControllerDep, limit: int = 20, offset: int = 0):
    return await controller.get_all(limit=limit, offset=offset)


@router.get("/{uid}")
async def get_by_uid(uid: UUID, controller: ProductControllerDep):
    return await controller.get_by_uid(uid)


@router.post("/")
async def create(data: ProductIn, controller: ProductControllerDep):
    return await controller.create(data)


@router.put("/{uid}")
async def update(uid: UUID, data: ProductUpdateIn, controller: ProductControllerDep):
    return await controller.update(uid, data)


@router.delete("/{uid}")
async def delete(uid: UUID, controller: ProductControllerDep):
    return await controller.delete(uid)
