from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import Enum as PG_ENUM
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .order_item import DBOrderItem


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    SHIPPED = "shipped"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"


class PaymentStatus(StrEnum):
    UNPAID = "unpaid"
    PAID = "paid"
    REFUNDED = "refunded"
    FAILED = "failed"


class DBOrder(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "orders"

    status: Mapped[OrderStatus] = mapped_column(
        PG_ENUM(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        PG_ENUM(PaymentStatus, name="payment_status"),
        default=PaymentStatus.UNPAID,
        nullable=False,
    )

    total_amount: Mapped[Decimal | None] = mapped_column(nullable=True)

    stripe_checkout_session_id: Mapped[str | None] = mapped_column(
        String(256), nullable=True
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        String(256), nullable=True
    )
    stripe_charge_id: Mapped[str | None] = mapped_column(String(256), nullable=True)

    # Foreign Key
    user_uid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uid", ondelete="CASCADE"), nullable=False
    )

    # Relationship
    items: Mapped[List["DBOrderItem"]] = relationship(
        "DBOrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Order(uid='{self.uid!r}', user_uid='{self.user_uid!r}')>"
