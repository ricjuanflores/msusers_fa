from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions, require_roles
from ms_fa.repositories import PermissionRepository
from ms_fa.schemas.permission import (
    PermissionCreateRequest,
    PermissionUpdateRequest,
)
from ms_fa.helpers.time import datetime_to_epoch

router = APIRouter()


def serialize_permission(permission):
    return {
        "id": permission.id,
        "name": permission.name,
        "fixed": permission.fixed,
        "created_at": datetime_to_epoch(permission.created_at),
    }


@router.get("/permissions")
async def list_permissions_paginated(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - Permission - list")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    result = permission_repo.all(
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return {
        "data": [serialize_permission(item) for item in result['items']],
        "pagination": {
            "page": result['page'],
            "pages": result['pages'],
            "per_page": result['per_page'],
            "prev": result['prev'],
            "next": result['next'],
            "total": result['total'],
        }
    }


@router.get("/permissions/list")
async def list_permissions(
    auth: AuthPayload = Depends(require_permissions("User - Permission - list")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    permissions = permission_repo.all(paginate=False, order='asc', order_column='name')
    return [serialize_permission(p) for p in permissions]


@router.post("/permission", status_code=201)
async def create_permission(
    data: PermissionCreateRequest,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    permission = permission_repo.add(data.model_dump())
    return serialize_permission(permission)


@router.get("/permission/{id}")
async def get_permission(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - Permission - detail")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    permission = permission_repo.find(id)
    return serialize_permission(permission)


@router.put("/permission/{id}")
async def update_permission(
    id: str,
    data: PermissionUpdateRequest,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    permission = permission_repo.update(id, data.model_dump(exclude_unset=True))
    return serialize_permission(permission)


@router.delete("/permission/{id}", status_code=204)
async def delete_permission(
    id: str,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    permission_repo = PermissionRepository(db)
    permission, success = permission_repo.delete(id)
    if not success:
        raise HTTPException(
            status_code=403,
            detail="It's not possible delete a permission with the attribute 'fixed' like true"
        )
    return None

