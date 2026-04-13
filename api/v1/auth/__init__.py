from fastapi import APIRouter

from .auth import router as auth_router
from .mfa import router as mfa_router
from .oauth import router as oauth_router
from .password import router as password_router

router = APIRouter()

router.include_router(auth_router, tags=["Authentication"])
router.include_router(password_router, prefix="/password", tags=["Password"])
router.include_router(mfa_router, prefix="/mfa", tags=["MFA"])
router.include_router(oauth_router, prefix="/oauth", tags=["OAUTH"])
