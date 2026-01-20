from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions, require_roles
from ms_fa.repositories import RoleRepository
from ms_fa.schemas.role import (
    RoleCreateRequest,
    RoleUpdateRequest,
    RoleSyncPermissionsRequest,
)
from ms_fa.helpers.time import datetime_to_epoch

router = APIRouter()


def serialize_role(role):
    return {
        "id": role.id,
        "name": role.name,
        "fixed": role.fixed,
        "created_at": datetime_to_epoch(role.created_at),
    }


def serialize_role_with_permissions(role):
    data = serialize_role(role)
    data["permissions"] = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in role.permissions
    ]
    return data


@router.get("/roles")
async def list_roles_paginated(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - Role - list")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    result = role_repo.all(
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return {
        "data": [serialize_role(item) for item in result['items']],
        "pagination": {
            "page": result['page'],
            "pages": result['pages'],
            "per_page": result['per_page'],
            "prev": result['prev'],
            "next": result['next'],
            "total": result['total'],
        }
    }


@router.get("/roles/list")
async def list_roles(
    auth: AuthPayload = Depends(require_permissions("User - Role - list")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    roles = role_repo.all(paginate=False, order='asc', order_column='name')
    return [serialize_role(role) for role in roles]


@router.post("/role", status_code=201)
async def create_role(
    data: RoleCreateRequest,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    role = role_repo.add(data.model_dump())
    return serialize_role(role)


@router.get("/role/{id}")
async def get_role(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - Role - detail")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    role = role_repo.find(id)
    return serialize_role_with_permissions(role)


@router.put("/role/{id}")
async def update_role(
    id: str,
    data: RoleUpdateRequest,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    role, success = role_repo.update(id, data.model_dump(exclude_unset=True))
    if not success:
        raise HTTPException(status_code=403, detail="It's not possible modify the root role")
    return serialize_role(role)


@router.post("/role/{id}/sync-permissions", status_code=204)
async def sync_role_permissions(
    id: str,
    data: RoleSyncPermissionsRequest,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    role_repo.sync_permissions(id, data.permissions)
    return None


@router.delete("/role/{id}", status_code=204)
async def delete_role(
    id: str,
    auth: AuthPayload = Depends(require_roles("root")),
    db: Session = Depends(get_db)
):
    role_repo = RoleRepository(db)
    role, success = role_repo.delete(id)
    if not success:
        raise HTTPException(
            status_code=403,
            detail="It's not possible delete a role with the attribute 'fixed' like true"
        )
    return None

