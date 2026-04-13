from datetime import timedelta

from fastapi import Response

from app.schemas.extras.token import Token
from core.config import config


def _set_cookie(response: Response, key: str, value: str, max_age: int) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE,
    )


def set_auth_cookies(
    data: Token,
    response: Response,
) -> None:
    _set_cookie(
        response,
        config.COOKIE_ACCESS_TOKEN_KEY,
        data.access_token,
        int(timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()),
    )
    _set_cookie(
        response,
        config.COOKIE_REFRESH_TOKEN_KEY,
        data.refresh_token,
        int(timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS).total_seconds()),
    )


def delete_auth_cookies(response: Response) -> None:
    response.delete_cookie(config.COOKIE_ACCESS_TOKEN_KEY)
    response.delete_cookie(config.COOKIE_REFRESH_TOKEN_KEY)
