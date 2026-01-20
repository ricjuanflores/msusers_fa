from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions
from ms_fa.repositories import UserRepository
from ms_fa.schemas.user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserUpdatePasswordRequest,
    UserSyncPermissionsRequest,
    UserSyncRolesRequest,
    UserUpdateAvailableCreditRequest,
)
from ms_fa.helpers.time import datetime_to_epoch
from ms_fa.routers.account import serialize_user_profile, serialize_profile

router = APIRouter()


def serialize_user(user):
    return {
        "id": user.id,
        "aq_id": user.aq_id,
        "email": user.email,
        "phone": user.phone,
        "name": user.name,
        "lastname": user.lastname,
        "second_lastname": user.second_lastname,
        "is_active": user.is_active,
        "created_at": datetime_to_epoch(user.created_at),
        "deleted_at": datetime_to_epoch(user.deleted_at) if user.deleted_at else None,
        "profile": {
            "rfc": user.profile.rfc if user.profile else None,
            "curp": user.profile.curp if user.profile else None,
        } if user.profile else None,
    }


def serialize_paginated(result, serializer):
    return {
        "data": [serializer(item) for item in result['items']],
        "pagination": {
            "page": result['page'],
            "pages": result['pages'],
            "per_page": result['per_page'],
            "prev": result['prev'],
            "next": result['next'],
            "total": result['total'],
        }
    }


@router.get("")
async def list_users(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - list")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    result = user_repo.all(
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return serialize_paginated(result, serialize_user)


@router.get("/trash")
async def list_trash(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - list")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    result = user_repo.all(
        deleted=True,
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return serialize_paginated(result, serialize_user)


@router.post("", status_code=201)
async def create_user(
    request: Request,
    data: UserCreateRequest,
    auth: AuthPayload = Depends(require_permissions("User - create")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user = user_repo.add(data.model_dump())
    return serialize_user(user)


@router.get("/{id}")
async def get_user(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - detail")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.find(id)
    return serialize_user_profile(user)


@router.get("/aq/{id}")
async def get_user_by_aq(
    id: int,
    auth: AuthPayload = Depends(require_permissions("User - detail")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.find_by_attr("aq_id", id)
    return serialize_user_profile(user)


@router.put("/{id}")
async def update_user(
    id: str,
    data: UserUpdateRequest,
    auth: AuthPayload = Depends(require_permissions("User - update")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.update(id, data.model_dump(exclude_unset=True))
    return serialize_user(user)


@router.put("/{id}/password", status_code=204)
async def update_user_password(
    id: str,
    data: UserUpdatePasswordRequest,
    auth: AuthPayload = Depends(require_permissions("User - update password")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_repo.update_password(id, data.password)
    return None


@router.get("/{id}/devices")
async def get_user_devices(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - detail")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.find(id)
    devices = [
        {
            "id": d.id,
            "device_id": d.device_id,
            "mark": d.mark,
            "model": d.model,
            "carrier": d.carrier,
            "os": d.os,
            "nfc": d.nfc,
            "app_version": d.app_version,
            "created_at": datetime_to_epoch(d.created_at),
        }
        for d in user.devices
    ]
    return devices


@router.get("/{id}/permissions")
async def get_user_permissions(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - detail")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.find(id)
    permissions = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in user.permissions.all()
    ]
    role_permissions = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in user.all_permissions
    ]
    return {
        "permissions": permissions,
        "roles_permissions": role_permissions,
    }


@router.post("/{id}/sync-permissions", status_code=204)
async def sync_user_permissions(
    id: str,
    request: Request,
    data: UserSyncPermissionsRequest,
    auth: AuthPayload = Depends(require_permissions("User - permissions")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user_repo.sync_permissions(id, data.permissions)
    return None


@router.post("/{id}/sync-roles", status_code=204)
async def sync_user_roles(
    id: str,
    request: Request,
    data: UserSyncRolesRequest,
    auth: AuthPayload = Depends(require_permissions("User - roles")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user_repo.sync_roles(id, data.roles)
    return None


@router.post("/{id}/activate", status_code=204)
async def activate_user(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - activate")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_repo.activate(id)
    return None


@router.delete("/{id}/activate", status_code=204)
async def deactivate_user(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - activate")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_repo.deactivate(id)
    return None


@router.delete("/{id}", status_code=204)
async def soft_delete_user(
    id: str,
    request: Request,
    auth: AuthPayload = Depends(require_permissions("User - soft delete")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user_repo.soft_delete(id)
    return None


@router.post("/{id}/restore", status_code=204)
async def restore_user(
    id: str,
    request: Request,
    auth: AuthPayload = Depends(require_permissions("User - restore")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user_repo.restore(id)
    return None


@router.delete("/{id}/hard", status_code=204)
async def delete_user(
    id: str,
    request: Request,
    auth: AuthPayload = Depends(require_permissions("User - delete")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user_repo.delete(id)
    return None

