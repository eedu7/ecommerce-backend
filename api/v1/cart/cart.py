from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


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
async def create():
    pass


@router.put("/{uid}")
async def update(uid: UUID):
    pass


@router.delete("/{uid}")
async def delete(uid: UUID):
    pass
