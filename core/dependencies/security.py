from typing import Annotated

from fastapi import Depends

from core.security import JWTService, PasswordService


def get_jwt_service() -> JWTService:
    return JWTService()


def get_password_service() -> PasswordService:
    return PasswordService()


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]
PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]
