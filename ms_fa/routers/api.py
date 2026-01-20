from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ms_fa.config import settings
from ms_fa.db import get_db, db_ping
from ms_fa.helpers.files import s3_ping
from ms_fa.middlewares import get_current_user, AuthPayload

from ms_fa.routers.auth import router as auth_router
from ms_fa.routers.account import router as account_router
from ms_fa.routers.admin import router as admin_router
from ms_fa.routers.roles import router as roles_router
from ms_fa.routers.permissions import router as permissions_router
from ms_fa.routers.shopper import router as shopper_router
from ms_fa.routers.apps import router as apps_router
from ms_fa.routers.devices import router as devices_router


api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(account_router, prefix="/profile", tags=["Account"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin Users"])
api_router.include_router(roles_router, prefix="/admin", tags=["Roles"])
api_router.include_router(permissions_router, prefix="/admin", tags=["Permissions"])
api_router.include_router(shopper_router, prefix="/shopper", tags=["Shopper"])
api_router.include_router(apps_router, prefix="/admin/apps", tags=["Apps"])
api_router.include_router(devices_router, prefix="/admin/device", tags=["Devices"])


@api_router.get("/")
async def api_index():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@api_router.get("/status")
async def api_status(
    request: Request,
    auth: AuthPayload = Depends(get_current_user)
):
    cache = getattr(request.app.state, 'cache', None)
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
        "services": {
            "cache": cache.ping() if cache else False,
            "storage": s3_ping(),
            "db": db_ping(),
        }
    }

