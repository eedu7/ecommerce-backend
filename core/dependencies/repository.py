from typing import Annotated

from fastapi import Depends

from app.repositories import (
    CartItemRepository,
    CartRepository,
    CategoryRepository,
    OrderItemRepository,
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from core.factory.repository import RepositoryFactory

UserRepositoryDep = Annotated[
    UserRepository, Depends(RepositoryFactory.get_user_repository)
]

CategoryRepositoryDep = Annotated[
    CategoryRepository, Depends(RepositoryFactory.get_category_repository)
]

ProductRepositoryDep = Annotated[
    ProductRepository, Depends(RepositoryFactory.get_product_repository)
]

CartRepositoryDep = Annotated[
    CartRepository, Depends(RepositoryFactory.get_cart_repository)
]

CartItemRepositoryDep = Annotated[
    CartItemRepository, Depends(RepositoryFactory.get_cart_item_repository)
]

OrderRepositoryDep = Annotated[
    OrderRepository, Depends(RepositoryFactory.get_order_repository)
]

OrderItemRepositoryDep = Annotated[
    OrderItemRepository, Depends(RepositoryFactory.get_order_item_repository)
]
