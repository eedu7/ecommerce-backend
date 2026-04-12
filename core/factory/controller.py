from app.controllers import AuthController, UserController
from core.dependencies.repository import UserRepositoryDep


class ControllerFactory:
    @staticmethod
    def get_user_controller(repository: UserRepositoryDep) -> UserController:
        return UserController(repository)

    @staticmethod
    def get_auth_controller(repository: UserRepositoryDep) -> AuthController:
        return AuthController(repository)
