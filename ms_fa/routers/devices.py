from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions
from ms_fa.repositories import DeviceRepository
from ms_fa.schemas.device import (
    DeviceCreateRequest,
    DeviceUpdateRequest,
)
from ms_fa.helpers.time import datetime_to_epoch

router = APIRouter()


def serialize_device(device):
    return {
        "id": device.id,
        "device_id": device.device_id,
        "mark": device.mark,
        "model": device.model,
        "carrier": device.carrier,
        "os": device.os,
        "nfc": device.nfc,
        "app_version": device.app_version,
        "user_id": device.user_id,
        "created_at": datetime_to_epoch(device.created_at),
    }


@router.get("")
async def list_devices(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    order: str = Query("desc"),
    order_column: str = Query("created_at"),
    q: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - Device - list")),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    result = device_repo.all(
        paginate=True,
        per_page=per_page,
        page=page,
        order=order,
        order_column=order_column,
        search=q,
    )
    return {
        "data": [serialize_device(item) for item in result['items']],
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
async def create_device(
    data: DeviceCreateRequest,
    auth: AuthPayload = Depends(require_permissions("User - Device - create")),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device = device_repo.add(data.model_dump())
    return serialize_device(device)


@router.get("/{id}")
async def get_device(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - Device - detail")),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device = device_repo.find(id)
    return serialize_device(device)


@router.put("/{id}")
async def update_device(
    id: str,
    data: DeviceUpdateRequest,
    auth: AuthPayload = Depends(require_permissions("User - Device - update")),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device = device_repo.update(id, data.model_dump(exclude_unset=True))
    return serialize_device(device)


@router.delete("/{id}", status_code=204)
async def delete_device(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - Device - delete")),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device_repo.delete(id)
    return None

