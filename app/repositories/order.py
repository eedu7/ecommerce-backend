from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBOrder
from core.repository import BaseRepository


class OrderRepository(BaseRepository[DBOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBOrder, session)
