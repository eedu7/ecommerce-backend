from fastapi import APIRouter, status

from app.schemas.requests.auth import AuthIn, AuthLogin
from app.schemas.responses.auth import AuthOut
from core.dependencies.controller import AuthControllerDep

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AuthOut)
async def register(data: AuthIn, controller: AuthControllerDep) -> AuthOut:
    return await controller.register(data)


@router.post("/login", response_model=AuthOut)
async def login(data: AuthLogin, controller: AuthControllerDep) -> AuthOut:
    return await controller.login(data)
