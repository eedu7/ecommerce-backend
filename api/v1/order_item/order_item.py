from uuid import UUID

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get():
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
