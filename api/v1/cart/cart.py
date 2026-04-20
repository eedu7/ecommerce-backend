from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.dependencies.auth import auth_required
from core.dependencies.controller import CartControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter(dependencies=[Depends(auth_required)])


@router.get("/")
async def get_carts():
    pass


@router.get("/{uid}")
async def get_cart(uid: UUID):
    pass


@router.get("/me")
async def get_user_cart():
    pass


@router.post("/")
async def create(user: CurrentUserDep, controller: CartControllerDep) -> JSONResponse:
    return await controller.create(user)


@router.put("/{uid}")
async def update(uid: UUID):
    pass


@router.delete("/{uid}")
async def delete(uid: UUID):
    pass
