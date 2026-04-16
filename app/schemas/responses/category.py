from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    uid: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)
