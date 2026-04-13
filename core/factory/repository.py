from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository


class RepositoryFactory:
    @staticmethod
    def get_user_repository(session: AsyncSession) -> UserRepository:
        return UserRepository(session)
