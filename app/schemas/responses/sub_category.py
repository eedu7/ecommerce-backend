from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubCategoryOut(BaseModel):
    uid: UUID
    name: str
    slug: str
    category_uid: UUID

    model_config = ConfigDict(from_attributes=True)
