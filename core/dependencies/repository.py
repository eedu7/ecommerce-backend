from typing import Annotated

from fastapi import Depends

from app.repositories import (
    CategoryRepository,
    ProductRepository,
    SubCategoryRepository,
    UserRepository,
)
from core.factory.repository import RepositoryFactory

UserRepositoryDep = Annotated[
    UserRepository, Depends(RepositoryFactory.get_user_repository)
]

CategoryRepositoryDep = Annotated[
    CategoryRepository, Depends(RepositoryFactory.get_category_repository)
]

SubCategoryRepositoryDep = Annotated[
    SubCategoryRepository, Depends(RepositoryFactory.get_sub_category_repository)
]

ProductRepositoryDep = Annotated[
    ProductRepository, Depends(RepositoryFactory.get_product_repository)
]
