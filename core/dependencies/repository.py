from typing import Annotated

from fastapi import Depends

from app.repositories import CategoryRepository, SubCategoryRepository, UserRepository
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
