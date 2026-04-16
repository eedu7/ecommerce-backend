from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.requests.sub_category import SubCategoryIn
from app.schemas.responses.sub_category import SubCategoryOut
from core.dependencies.controller import SubCategoryControllerDep

router = APIRouter()


@router.get("/")
async def get():
    pass


@router.get("/{uid}")
async def get_by_uid(uid: UUID):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SubCategoryOut)
async def create(data: SubCategoryIn, controller: SubCategoryControllerDep):

    return await controller.create(data)


@router.put("/{uid}")
async def update(uid: UUID):
    pass


@router.delete("/{uid}")
async def delete(uid: UUID):
    pass
