from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse

from app.models import DBUser
from app.schemas.requests.auth import AuthIn, AuthLogin, AuthLogout
from app.schemas.responses.auth import AuthOut
from app.schemas.responses.user import UserOut
from core.dependencies.auth import auth_required
from core.dependencies.controller import AuthControllerDep
from core.dependencies.user import CurrentUserDep

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AuthOut)
async def register(
    data: AuthIn, response: Response, controller: AuthControllerDep
) -> AuthOut:
    return await controller.register(data, response)


@router.post("/login", response_model=AuthOut)
async def login(
    data: AuthLogin, response: Response, controller: AuthControllerDep
) -> AuthOut:
    return await controller.login(data, response)


@router.post("/logout")
async def logout(
    data: AuthLogout,
    request: Request,
    response: Response,
    controller: AuthControllerDep,
) -> JSONResponse:
    return await controller.logout(data=data, response=response, request=request)


@router.get(
    "/me",
    response_model=UserOut,
    dependencies=[Depends(auth_required)],
)
async def get_me(current_user: CurrentUserDep) -> DBUser:
    return current_user
