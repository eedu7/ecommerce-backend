from datetime import datetime
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

TokenType = Literal["access", "refresh"]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    type: TokenType
    jti: str
    iat: datetime
    exp: datetime
    nbf: datetime | None = None
    iss: str | None = None
    aud: str | None = None
    extra: Dict[str, Any] = Field(default_factory=dict)
