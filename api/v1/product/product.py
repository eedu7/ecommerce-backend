from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.requests.product import ProductIn, ProductUpdateIn
from app.schemas.responses.product import ProductOut
from core.dependencies.controller import ProductControllerDep

router = APIRouter()


@router.get("/", response_model=List[ProductOut])
async def get_all(controller: ProductControllerDep, limit: int = 20, offset: int = 0):
    return await controller.get_all(limit=limit, offset=offset)


@router.get("/{uid}", response_model=ProductOut)
async def get_by_uid(uid: UUID, controller: ProductControllerDep):
    return await controller.get_by_uid(uid)


@router.post("/", response_model=ProductOut)
async def create(data: ProductIn, controller: ProductControllerDep):
    return await controller.create(data)


@router.put("/{uid}", response_model=ProductOut)
async def update(uid: UUID, data: ProductUpdateIn, controller: ProductControllerDep):
    return await controller.update(uid, data)


@router.delete("/{uid}")
async def delete(uid: UUID, controller: ProductControllerDep) -> JSONResponse:
    return await controller.delete(uid)
