from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBCart
from core.repository import BaseRepository


class CartRepository(BaseRepository[DBCart]):
    def __init__(self, session: AsyncSession):
        super().__init__(DBCart, session)
