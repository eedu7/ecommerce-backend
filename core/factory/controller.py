from app.controllers import AuthController, CategoryController, UserController
from core.dependencies.repository import (
    CategoryRepositoryDep,
    SubCategoryRepositoryDep,
    UserRepositoryDep,
)
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

    @staticmethod
    def get_category_controller(
        category_repository: CategoryRepositoryDep,
        sub_category_repository: SubCategoryRepositoryDep,
    ) -> CategoryController:
        return CategoryController(category_repository, sub_category_repository)
