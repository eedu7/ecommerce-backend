from typing import Annotated

from fastapi import Depends

from core.security import (
    JWTService,
    PasswordService,
    get_jwt_service,
    get_password_service,
)


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]
PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]
