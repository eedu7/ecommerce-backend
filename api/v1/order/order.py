from fastapi import APIRouter

from core.dependencies.controller import OrderControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter()


@router.get("/")
async def get_current_user_orders(
    current_user: CurrentUserDep, controller: OrderControllerDep
):
    return await controller.get_user_orders(current_user.uid)


# TODO: Added the Create Order API Endpoint
# @router.post("/")
# async def create():
#     pass


# TODO: Added the Update Order API Endpoint
# @router.put("/{uid}")
# async def update(uid: UUID):
#     pass


# TODO: Added the Delete Order API Endpoint
# @router.delete("/{uid}")
# async def delete(uid: UUID):
#     pass
