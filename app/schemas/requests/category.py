from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str


class CategoryUpdateIn(BaseModel):
    name: str | None = None
    slug: str | None = None
