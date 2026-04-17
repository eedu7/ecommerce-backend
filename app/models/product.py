from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .category import DBCategory  # Avoid circular import for type checking


class DBProduct(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    slug: Mapped[str] = mapped_column(
        String(320), nullable=False, unique=True, index=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )

    # Foreign Key
    category_uid: Mapped[UUID] = mapped_column(
        ForeignKey("categories.uid", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    category: Mapped["DBCategory"] = relationship(
        "DBCategory", back_populates="products"
    )

    def __repr__(self) -> str:
        return (
            f"<Product(uid='{self.uid!r}', name='{self.name!r}', slug='{self.slug!r}')>"
        )
