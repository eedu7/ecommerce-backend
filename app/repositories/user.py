from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBUser
from core.repository import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBUser, session)
