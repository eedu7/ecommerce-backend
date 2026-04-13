from app.controllers import AuthController, UserController
from core.dependencies.repository import UserRepositoryDep
from core.dependencies.security import JWTServiceDep, PasswordServiceDep


class ControllerFactory:
    @staticmethod
    def get_user_controller(repository: UserRepositoryDep) -> UserController:
        return UserController(repository)

    @staticmethod
    def get_auth_controller(
        repository: UserRepositoryDep, jwt: JWTServiceDep, password: PasswordServiceDep
    ) -> AuthController:
        return AuthController(repository, jwt, password)
