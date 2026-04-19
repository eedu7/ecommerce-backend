from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBCartItem
from core.repository import BaseRepository


class CartItemRepository(BaseRepository[DBCartItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBCartItem, session)
