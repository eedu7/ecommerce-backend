from typing import Annotated

from fastapi import Depends

from app.controllers import (
    AuthController,
    CartController,
    CartItemController,
    CategoryController,
    OrderController,
    OrderItemController,
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

CartControllerDep = Annotated[
    CartController, Depends(ControllerFactory.get_cart_controller)
]

CartItemControllerDep = Annotated[
    CartItemController, Depends(ControllerFactory.get_cart_item_controller)
]

OrderControllerDep = Annotated[
    OrderController, Depends(ControllerFactory.get_order_controller)
]

OrderItemControllerDep = Annotated[
    OrderItemController, Depends(ControllerFactory.get_order_item_controller)
]
