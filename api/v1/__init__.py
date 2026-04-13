from fastapi import APIRouter

from .auth import router as auth_router
from .category import category_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(category_router, prefix="/categories", tags=["Categories"])
