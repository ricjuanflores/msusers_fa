from fastapi import FastAPI

from ms_fa.routers.api import api_router
from ms_fa.routers.web import web_router


def register_routers(app: FastAPI):
    app.include_router(web_router)
    app.include_router(api_router, prefix="/api/v1/users")

