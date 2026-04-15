from uuid import UUID

from pydantic import BaseModel


class SubCategoryIn(BaseModel):
    name: str
    parent_uid: UUID
