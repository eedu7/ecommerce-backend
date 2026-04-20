from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .cart_item import DBCartItem


class DBCart(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "carts"

    # Foreign Key
    user_uid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uid", ondelete="CASCADE"), nullable=False, unique=True
    )

    # Relationship
    items: Mapped[List["DBCartItem"]] = relationship(
        "DBCartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cart(uid='{self.uid!r}', user_uid='{self.user_uid!r}')>"
