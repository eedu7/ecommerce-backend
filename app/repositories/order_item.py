from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBOrderItem
from core.repository import BaseRepository


class OrderItemRepository(BaseRepository[DBOrderItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBOrderItem, session)
