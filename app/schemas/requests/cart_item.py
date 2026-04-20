from uuid import UUID

from pydantic import BaseModel


class CartItemIn(BaseModel):
    quantity: int = 0
    product_uid: UUID
