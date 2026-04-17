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


class ProductUpdateIn(BaseModel):
    name: str | None = None
    description: str | None = None
    category_uid: UUID | None = None
    sub_category_uid: UUID | None = None
    price: float | None = None
    stock_quantity: int | None = None
    is_active: bool | None = None
    is_featured: bool | None = None
