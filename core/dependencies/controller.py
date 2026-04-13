from typing import Annotated

from fastapi import Depends

from app.controllers import AuthController, CategoryController, UserController
from core.factory.controller import ControllerFactory

UserControllerDep = Annotated[
    UserController, Depends(ControllerFactory.get_user_controller)
]

AuthControllerDep = Annotated[
    AuthController, Depends(ControllerFactory.get_auth_controller)
]

CategoryControllerDep = Annotated[
    CategoryController, Depends(ControllerFactory.get_category_controller)
]
