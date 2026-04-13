from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController
from core.security import JWTService, PasswordService


class AuthController(BaseController[DBUser]):
    def __init__(
        self, repository: UserRepository, jwt: JWTService, password: PasswordService
    ) -> None:
        super().__init__(DBUser, repository)
        self.repository = repository
        self.jwt = jwt
        self.password = password
