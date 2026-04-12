from uuid import UUID, uuid4

from sqlalchemy import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    uid: Mapped[UUID] = mapped_column(
        PG_UUID(),
        index=True,
        default=uuid4,
        sort_order=-32,
        primary_key=True,
    )
