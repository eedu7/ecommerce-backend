from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBUser
from core.repository import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBUser, session)

    async def get_by_email(self, email: str) -> DBUser | None:
        return await self.get_one_by_filters({"email": email})

    async def get_by_username(self, username: str) -> DBUser | None:
        return await self.get_one_by_filters({"username": username})
