from fastapi import APIRouter

router = APIRouter()


@router.post("/forgot")
async def forgot_password():
    pass


@router.post("/reset")
async def reset_password():
    pass


@router.post("/change")
async def change_password():
    pass
