from typing import Annotated

from fastapi import Depends

from app.repositories import UserRepository
from core.dependencies.session import AsyncSessionDep
from core.factory.repository import RepositoryFactory


def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return RepositoryFactory.get_user_repository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
