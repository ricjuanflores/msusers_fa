from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions
from ms_fa.repositories import AppRepository
from ms_fa.helpers.jwt import JwtHelper
from ms_fa.schemas.app import (
    AppCreateRequest,
    AppUpdateRequest,
    AppSyncPermissionsRequest,
    AppSyncRolesRequest,
)
from ms_fa.helpers.time import datetime_to_epoch

router = APIRouter()


def serialize_app(app):
    return {
        "id": app.id,
        "name": app.name,
        "description": app.description,
        "created_at": datetime_to_epoch(app.created_at),
    }


@router.get("")
async def list_apps(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - App - list")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    result = app_repo.all(
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return {
        "data": [serialize_app(item) for item in result['items']],
        "pagination": {
            "page": result['page'],
            "pages": result['pages'],
            "per_page": result['per_page'],
            "prev": result['prev'],
            "next": result['next'],
            "total": result['total'],
        }
    }


@router.post("", status_code=201)
async def create_app(
    data: AppCreateRequest,
    auth: AuthPayload = Depends(require_permissions("User - App - create")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    app = app_repo.add(data.model_dump())
    return serialize_app(app)


@router.get("/{id}")
async def get_app(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - App - detail")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    app = app_repo.find(id)
    return serialize_app(app)


@router.post("/{id}/token")
async def generate_app_token(
    id: str,
    request: Request,
    auth: AuthPayload = Depends(require_permissions("User - App - generate token")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=1576800000)
    app_repo = AppRepository(db, cache)
    
    app = app_repo.find(id)
    payload = {"id": app.id}
    token = jwt_helper.get_tokens(payload)
    app_repo.update_token(app, token.get('token'))
    
    return token


@router.put("/{id}")
async def update_app(
    id: str,
    data: AppUpdateRequest,
    auth: AuthPayload = Depends(require_permissions("User - App - update")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    app = app_repo.update(id, data.model_dump(exclude_unset=True))
    return serialize_app(app)


@router.get("/{id}/permissions")
async def get_app_permissions(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - App - detail")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    app = app_repo.find(id)
    permissions = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in app.permissions.all()
    ]
    role_permissions = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in app.all_permissions
    ]
    return {
        "permissions": permissions,
        "roles_permissions": role_permissions,
    }


@router.post("/{id}/sync-permissions", status_code=204)
async def sync_app_permissions(
    id: str,
    request: Request,
    data: AppSyncPermissionsRequest,
    auth: AuthPayload = Depends(require_permissions("User - App - permissions")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    app_repo = AppRepository(db, cache)
    app_repo.sync_permissions(id, data.permissions)
    return None


@router.post("/{id}/sync-roles", status_code=204)
async def sync_app_roles(
    id: str,
    request: Request,
    data: AppSyncRolesRequest,
    auth: AuthPayload = Depends(require_permissions("User - App - roles")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    app_repo = AppRepository(db, cache)
    app_repo.sync_roles(id, data.roles)
    return None


@router.delete("/{id}", status_code=204)
async def delete_app(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - App - delete")),
    db: Session = Depends(get_db)
):
    app_repo = AppRepository(db)
    app_repo.delete(id)
    return None

