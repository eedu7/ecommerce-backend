from enum import StrEnum

from sqlalchemy import Enum as PG_Enum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin


class DBUserRole(StrEnum):
    ADMIN = "admin"
    TENANT_OWNER = "tenant_owner"
    TENANT_ADMIN = "tenant_admin"
    TENANT_STAFF = "tenant_staff"
    TENANT_VIEWER = "tenant_viewer"
    CUSTOMER = "customer"


class DBUser(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=True)
    role: Mapped[DBUserRole] = mapped_column(
        PG_Enum(DBUserRole), nullable=False, default=DBUserRole.CUSTOMER
    )

    def __repr__(self):
        return f"<DBUser(username='{self.username}', email='{self.email}')>"
