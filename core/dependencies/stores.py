from typing import Annotated

from fastapi import Depends

from core.stores import RevokeTokenStore, get_revoke_token_store

RevokeTokenStoreDep = Annotated[RevokeTokenStore, Depends(get_revoke_token_store)]
