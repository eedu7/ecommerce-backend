from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubCategoryOut(BaseModel):
    uid: UUID
    name: str
    parent_uid: UUID

    model_config = ConfigDict(from_attributes=True)
