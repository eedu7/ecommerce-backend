from app.controllers import (
    AuthController,
    CategoryController,
    ProductController,
    SubCategoryController,
    UserController,
)
from core.dependencies.repository import (
    CategoryRepositoryDep,
    ProductRepositoryDep,
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
        repository: CategoryRepositoryDep,
    ) -> CategoryController:
        return CategoryController(repository)

    @staticmethod
    def get_sub_category_controller(
        repository: SubCategoryRepositoryDep,
    ) -> SubCategoryController:
        return SubCategoryController(repository)

    @staticmethod
    def get_product_controller(repository: ProductRepositoryDep) -> ProductController:
        return ProductController(repository)
