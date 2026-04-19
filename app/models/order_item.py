from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .order import DBOrder
    from .product import DBProduct


class DBOrderItem(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "order_items"

    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Foreign Keys
    order_uid: Mapped[UUID] = mapped_column(
        ForeignKey("orders.uid", ondelete="CASCADE"), nullable=False
    )
    product_uid: Mapped[UUID] = mapped_column(
        ForeignKey("products.uid", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    order: Mapped["DBOrder"] = relationship("DBOrder", back_populates="items")
    product: Mapped["DBProduct"] = relationship("DBProduct")

    def __repr__(self) -> str:
        return f"<OrderItem(uid='{self.uid!r}', product_uid='{self.product_uid!r}', quantity={self.quantity})>"
