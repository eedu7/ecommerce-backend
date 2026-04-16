from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.requests.sub_category import SubCategoryIn, SubCategoryUpdateIn
from app.schemas.responses.sub_category import SubCategoryOut
from core.dependencies.controller import SubCategoryControllerDep

router = APIRouter()


@router.get("/")
async def get():
    pass


@router.get("/{uid}", response_model=SubCategoryOut)
async def get_by_uid(uid: UUID, controller: SubCategoryControllerDep):
    return await controller.get_by_uid(uid)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SubCategoryOut)
async def create(data: SubCategoryIn, controller: SubCategoryControllerDep):
    return await controller.create(data)


@router.put("/{uid}", response_model=SubCategoryOut)
async def update(
    uid: UUID, data: SubCategoryUpdateIn, controller: SubCategoryControllerDep
):
    return await controller.update(uid, data)


@router.delete("/{uid}")
async def delete(uid: UUID, controller: SubCategoryControllerDep) -> JSONResponse:
    return await controller.delete(uid)
