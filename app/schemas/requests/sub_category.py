from uuid import UUID

from pydantic import BaseModel


class SubCategoryIn(BaseModel):
    name: str
    category_uid: UUID


class SubCategoryUpdateIn(BaseModel):
    name: str | None = None
    slug: str | None = None
    category_uid: UUID | None = None
