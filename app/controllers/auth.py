from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController


class AuthController(BaseController[DBUser]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(DBUser, repository)
        self.repository = repository
