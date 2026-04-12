from fastapi import FastAPI

from api import router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def run_server() -> FastAPI:
    app_ = FastAPI(title="ECommerce Backend")
    init_routers(app_)
    return app_
