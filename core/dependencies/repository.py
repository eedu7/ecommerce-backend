from typing import Annotated

from fastapi import Depends

from app.repositories import UserRepository
from core.factory import RepositoryFactory

UserRepositoryDep = Annotated[
    UserRepository, Depends(RepositoryFactory.get_user_repository)
]
