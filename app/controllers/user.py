from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController


class UserController(BaseController[DBUser]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(DBUser, repository)
        self.repository = repository
