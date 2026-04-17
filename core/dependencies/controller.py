from typing import Annotated

from fastapi import Depends

from app.controllers import (
    AuthController,
    CategoryController,
    ProductController,
    UserController,
)
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

ProductControllerDep = Annotated[
    ProductController, Depends(ControllerFactory.get_product_controller)
]
