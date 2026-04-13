from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .sub_category import DBSubCategory  # Avoid circular import for type checking


class DBCategory(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(84), nullable=False, unique=True)

    # Relationship to sub-categories
    sub_categories: Mapped[list["DBSubCategory"]] = relationship(
        "DBSubCategory", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Category(id={self.uid!r}, name='{self.name!r}', slug='{self.slug!r}')>"
        )
