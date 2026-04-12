from typing import Annotated

from fastapi import Depends

from app.controllers import AuthController, UserController
from core.factory import ControllerFactory

UserControllerDep = Annotated[
    UserController, Depends(ControllerFactory.get_user_controller)
]

AuthControllerDep = Annotated[
    AuthController, Depends(ControllerFactory.get_auth_controller)
]
