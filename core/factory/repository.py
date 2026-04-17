from app.repositories import (
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
