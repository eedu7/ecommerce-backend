from uuid import UUID

from pydantic import BaseModel


class CurrentUser(BaseModel):
    uid: UUID | None = None
