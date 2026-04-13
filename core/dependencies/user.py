from typing import Annotated

from fastapi import Depends, Request

from app.models import DBUser
from core.dependencies.controller import UserControllerDep


async def get_current_user(request: Request, controller: UserControllerDep) -> DBUser:
    return await controller.get_by_uid(request.state.user.uid)


CurrentUserDep = Annotated[DBUser, Depends(get_current_user)]
