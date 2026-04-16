from uuid import UUID

from pydantic import BaseModel


class SubCategoryIn(BaseModel):
    name: str
    category_uid: UUID
