from pydantic import BaseModel

from app.schemas.extras.token import Token
from app.schemas.responses.user import UserOut


class AuthOut(BaseModel):
    token: Token
    user: UserOut
