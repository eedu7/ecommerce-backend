from pydantic import BaseModel

from app.schemas.responses.category import CategoryOut


class ProductOut(BaseModel):
    name: str
    description: str | None
    slug: str
    price: float
    stock_quantity: int
    is_active: bool
    is_featured: bool
    category: CategoryOut
