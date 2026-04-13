from uuid import UUID

from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class UserController(BaseController[DBUser]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(DBUser, repository)
        self.repository = repository

    async def get_by_uid(self, uid: UUID) -> DBUser:
        user = await self.repository.get_by_uid(uid)
        if not user:
            raise NotFoundException()
        return user
