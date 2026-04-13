from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.config import config


def make_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ALLOW_ORIGINS,
        allow_credentials=config.CORS_ALLOW_CREDENTIALS,
        allow_methods=config.CORS_ALLOW_METHODS,
        allow_headers=config.CORS_ALLOW_HEADERS,
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def run_server() -> FastAPI:
    app_ = FastAPI(title="ECommerce Backend")
    init_routers(app_)
    make_middleware(app_)
    return app_
