from app.controllers import (
    AuthController,
    CartController,
    CartItemController,
    CategoryController,
    ProductController,
    UserController,
)
from core.dependencies.repository import (
    CartItemRepositoryDep,
    CartRepositoryDep,
    CategoryRepositoryDep,
    ProductRepositoryDep,
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
    def get_product_controller(repository: ProductRepositoryDep) -> ProductController:
        return ProductController(repository)

    @staticmethod
    def get_cart_controller(repository: CartRepositoryDep) -> CartController:
        return CartController(repository)

    @staticmethod
    def get_cart_item_controller(
        repository: CartItemRepositoryDep,
    ) -> CartItemController:
        return CartItemController(repository)
