from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from ms_fa.db import get_db
from ms_fa.middlewares import get_current_user, AuthPayload, require_permissions
from ms_fa.repositories import UserRepository, ShopperRepository, DeviceRepository
from ms_fa.schemas.user import (
    AccountUpdateRequest,
    AccountUpdateAuthRequest,
    AccountUpdatePasswordRequest,
    UserProfileResponse,
)
from ms_fa.schemas.profile import ProfileUpdateRequest, ProfilePatchRequest
from ms_fa.schemas.permission import PermissionResponse
from ms_fa.schemas.device import DeviceResponse, DeviceCreateRequest
from ms_fa.helpers.time import datetime_to_epoch

router = APIRouter()


def serialize_user_profile(user):
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
        "profile": serialize_profile(user.profile) if user.profile else None,
        "permissions": [{"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)} for p in user.all_permissions],
        "roles": [{"id": r.id, "name": r.name, "fixed": r.fixed, "created_at": datetime_to_epoch(r.created_at)} for r in user.roles],
    }


def serialize_profile(profile):
    if not profile:
        return None
    return {
        "rfc": profile.rfc,
        "curp": profile.curp,
        "home_phone": profile.home_phone,
        "birthday": profile.birthday.strftime("%Y-%m-%d") if profile.birthday else None,
        "entity_birth": profile.entity_birth,
        "entity_birth_name": profile.entity_birth_name,
        "gender": profile.gender,
        "grade": profile.grade,
        "marital_status": profile.marital_status,
        "municipality": profile.municipality,
        "state": profile.state,
        "state_name": profile.state_name,
        "country": profile.country,
        "street": profile.street,
        "reference_street": profile.reference_street,
        "reference_street_other": profile.reference_street_other,
        "additional_reference": profile.additional_reference,
        "exterior": profile.exterior,
        "interior": profile.interior,
        "neighborhood": profile.neighborhood,
        "zip": profile.zip,
        "department": profile.department,
        "monthly_expenditure": profile.monthly_expenditure,
        "income": profile.income,
        "income_family": profile.income_family,
        "count_home": profile.count_home,
        "count_income_people": profile.count_income_people,
        "company_name": profile.company_name,
        "type_activity": profile.type_activity,
        "position": profile.position,
        "time_activity_year": profile.time_activity_year,
        "time_activity_month": profile.time_activity_month,
        "available_credit": profile.available_credit,
        "pay_id": profile.pay_id,
        "payment_capacity": profile.payment_capacity,
        "second_credit": profile.second_credit,
        "personal_references": profile.personal_references or [],
        "kyc_prescoring_id": profile.kyc_prescoring_id,
        "legal_id_front": profile.legal_id_front,
        "legal_id_back": profile.legal_id_back,
        "proof_of_address": profile.proof_of_address,
    }


@router.get("")
async def get_profile(
    auth: AuthPayload = Depends(get_current_user)
):
    return serialize_user_profile(auth.user)


@router.put("")
async def update_profile(
    request: Request,
    data: ProfileUpdateRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update profile")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    user = shopper_repo.update(auth.user, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.patch("")
async def patch_profile(
    request: Request,
    data: ProfilePatchRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update profile")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    user = shopper_repo.update(auth.user, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.put("/account")
async def update_account(
    request: Request,
    data: AccountUpdateRequest,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user = user_repo.update(auth.user.id, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.put("/auth")
async def update_auth(
    request: Request,
    data: AccountUpdateAuthRequest,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    user = user_repo.update(auth.user.id, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.post("/update-password", status_code=204)
async def update_password(
    data: AccountUpdatePasswordRequest,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_repo.update_password(auth.user.id, data.password)
    return None


@router.get("/permissions")
async def get_permissions(
    auth: AuthPayload = Depends(get_current_user)
):
    permissions = [
        {"id": p.id, "name": p.name, "fixed": p.fixed, "created_at": datetime_to_epoch(p.created_at)}
        for p in auth.user.all_permissions
    ]
    return permissions


@router.get("/devices")
async def get_devices(
    auth: AuthPayload = Depends(get_current_user)
):
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
        for d in auth.user.devices
    ]
    return devices


@router.post("/devices", status_code=201)
async def add_device(
    data: DeviceCreateRequest,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    device_repo = DeviceRepository(db)
    device_data = data.model_dump()
    device_data['user_id'] = auth.user.id
    device = device_repo.add(device_data)
    return {
        "id": device.id,
        "device_id": device.device_id,
        "mark": device.mark,
        "model": device.model,
        "carrier": device.carrier,
        "os": device.os,
        "nfc": device.nfc,
        "app_version": device.app_version,
        "created_at": datetime_to_epoch(device.created_at),
    }

