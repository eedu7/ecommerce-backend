from app.repositories import (
    CartItemRepository,
    CartRepository,
    CategoryRepository,
    ProductRepository,
    UserRepository,
)
from core.dependencies.session import AsyncSessionDep


class RepositoryFactory:
    @staticmethod
    def get_user_repository(session: AsyncSessionDep) -> UserRepository:
        return UserRepository(session)

    @staticmethod
    def get_category_repository(session: AsyncSessionDep) -> CategoryRepository:
        return CategoryRepository(session)

    @staticmethod
    def get_product_repository(session: AsyncSessionDep) -> ProductRepository:
        return ProductRepository(session)

    @staticmethod
    def get_cart_repository(session: AsyncSessionDep) -> CartRepository:
        return CartRepository(session)

    @staticmethod
    def get_cart_item_repository(session: AsyncSessionDep) -> CartItemRepository:
        return CartItemRepository(session)
