from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.requests.category import CategoryIn, CategoryUpdateIn
from app.schemas.responses.category import CategoryOut
from core.dependencies.controller import CategoryControllerDep

router = APIRouter()


@router.get("/")
async def get_all(controller: CategoryControllerDep):
    pass


@router.get("/{uid}")
async def get_by_uid(uid: UUID):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryOut)
async def create(data: CategoryIn, controller: CategoryControllerDep):
    return await controller.create(data)


@router.put("/{uid}", response_model=CategoryOut)
async def update(uid: UUID, data: CategoryUpdateIn, controller: CategoryControllerDep):
    return await controller.update(uid, data)


@router.delete("/{uid}")
async def delete(uid: UUID, controller: CategoryControllerDep) -> JSONResponse:
    return await controller.delete(uid)
