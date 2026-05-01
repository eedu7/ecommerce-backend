from app.controllers import (
    AuthController,
    CartController,
    CartItemController,
    CategoryController,
    OrderController,
    OrderItemController,
    ProductController,
    UserController,
)
from core.dependencies.repository import (
    CartItemRepositoryDep,
    CartRepositoryDep,
    CategoryRepositoryDep,
    OrderItemRepositoryDep,
    OrderRepositoryDep,
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

    @staticmethod
    def get_order_controller(
        order_repository: OrderRepositoryDep,
        order_item_repository: OrderItemRepositoryDep,
        cart_repository: CartRepositoryDep,
        cart_item_repository: CartItemRepositoryDep,
    ) -> OrderController:
        return OrderController(
            order_repository=order_repository,
            order_item_repository=order_item_repository,
            cart_item_repository=cart_item_repository,
            cart_repository=cart_repository,
        )

    @staticmethod
    def get_order_item_controller(
        repository: OrderItemRepositoryDep,
    ) -> OrderItemController:
        return OrderItemController(repository)
