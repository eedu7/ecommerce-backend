from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .category import DBCategory  # Avoid circular import for type checking


class DBSubCategory(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sub_categories"

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(84), nullable=False, unique=True)

    # Foreign key to the parent category
    category_uid: Mapped[UUID] = mapped_column(
        ForeignKey("categories.uid", ondelete="CASCADE"), nullable=False
    )

    # Relationship to the parent category
    category: Mapped["DBCategory"] = relationship(
        "DBCategory", back_populates="sub_categories"
    )

    def __repr__(self) -> str:
        return f"<SubCategory(id={self.uid!r}, name='{self.name!r}', slug='{self.slug!r}')>"
