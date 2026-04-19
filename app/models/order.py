from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin


class DBOrder(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "orders"

    # Foreign Key
    user_uid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uid", ondelete="CASCADE"), nullable=False, unique=True
    )

    def __repr__(self) -> str:
        return f"<Order(uid='{self.uid!r}', user_uid='{self.user_uid!r}')>"
