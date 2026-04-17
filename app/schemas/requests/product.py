from uuid import UUID

from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    category_uid: UUID | None = None
    sub_category_uid: UUID | None = None
    price: float
    stock_quantity: int = 0
    is_active: bool = False
    is_featured: bool = False
