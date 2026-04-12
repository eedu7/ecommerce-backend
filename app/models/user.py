from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import DBBase
from core.database.mixin import PrimaryKeyMixin, TimestampMixin


class DBUser(DBBase, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=True)

    def __repr__(self):
        return f"<DBUser(username='{self.username}', email='{self.email}')>"
