from uuid import UUID

from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str
    parent_uid: UUID | None = None
