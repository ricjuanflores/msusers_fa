from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from ms_fa.config import settings
from ms_fa.db import engine, Base
from ms_fa.db.cache import Cache
from ms_fa.routers import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.cache = Cache(settings.redis_config)
    yield
    # Shutdown
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)

    return app


app = create_app()

