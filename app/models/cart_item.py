from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .cart import DBCart
    from .product import DBProduct


class DBCartItem(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "cart_items"

    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Foreign Keys
    cart_uid: Mapped[UUID] = mapped_column(
        ForeignKey("carts.uid", ondelete="CASCADE"), nullable=False
    )
    product_uid: Mapped[UUID] = mapped_column(
        ForeignKey("products.uid", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    cart: Mapped["DBCart"] = relationship("DBCart", back_populates="items")
    product: Mapped["DBProduct"] = relationship("DBProduct")

    def __repr__(self) -> str:
        return f"<CartItem(uid='{self.uid!r}',product_uid='{self.product_uid!r}', quantity={self.quantity})>"
