from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    uid: UUID
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
