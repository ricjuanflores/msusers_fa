from fastapi import APIRouter, Depends, Request, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional

from ms_fa.db import get_db
from ms_fa.middlewares import AuthPayload, require_permissions
from ms_fa.repositories import UserRepository, ShopperRepository
from ms_fa.models import Profile, User
from ms_fa.schemas.shopper import (
    ShopperCreateRequest,
    ShopperUpdateRequest,
    ShopperPatchRequest,
    ShopperUpdatePaymentRequest,
    ShopperUpdateAvailableCreditRequest,
    ShopperUpdatePaymentCapacityRequest,
)
from ms_fa.routers.account import serialize_user_profile
from sqlalchemy import func

router = APIRouter()


@router.post("", status_code=201)
async def create_shopper(
    request: Request,
    data: ShopperCreateRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - create")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    user = shopper_repo.add(data.model_dump())
    return serialize_user_profile(user)


@router.get("/unrelated")
async def list_unrelated_shoppers(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=100),
    search: Optional[str] = None,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - list")),
    db: Session = Depends(get_db)
):
    filters = [Profile.payment_capacity == 0]
    filters_search = []
    
    if search:
        page = 1
        filters_search.append(User.email == search)
        filters_search.append(User.phone == search)
        filters_search.append(func.concat(User.name, " ", User.lastname, " ", User.second_lastname) == search)
    
    shopper_repo = ShopperRepository(db)
    result = shopper_repo.find_all_optional(
        filters,
        filters_search,
        paginate=True,
        per_page=per_page,
        page=page
    )
    
    return {
        "data": [serialize_user_profile(user) for user in result['items']],
        "pagination": {
            "page": result['page'],
            "pages": result['pages'],
            "per_page": result['per_page'],
            "prev": result['prev'],
            "next": result['next'],
            "total": result['total'],
        }
    }


@router.get("/{id}")
async def get_shopper(
    id: str,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - detail")),
    db: Session = Depends(get_db)
):
    shopper_repo = ShopperRepository(db)
    user = shopper_repo.find_optional({"id": id, "phone": id, "email": id})
    return serialize_user_profile(user)


@router.put("/{id}")
async def update_shopper(
    id: str,
    request: Request,
    data: ShopperUpdateRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    shopper_repo = ShopperRepository(db, cache)
    
    user_data = {
        "name": data.name,
        "lastname": data.lastname,
        "second_lastname": data.second_lastname,
    }
    user = user_repo.update(id, {k: v for k, v in user_data.items() if v is not None})
    user = shopper_repo.update(user, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.patch("/{id}")
async def patch_shopper(
    id: str,
    request: Request,
    data: ShopperPatchRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    shopper_repo = ShopperRepository(db, cache)
    
    user_attrs = ["name", "lastname", "second_lastname"]
    user_data = {k: v for k, v in data.model_dump(exclude_unset=True).items() if k in user_attrs}
    
    user = user_repo.update(id, user_data)
    user = shopper_repo.update(user, data.model_dump(exclude_unset=True))
    return serialize_user_profile(user)


@router.put("/{id}/payment", status_code=204)
async def update_payment(
    id: str,
    request: Request,
    data: ShopperUpdatePaymentRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update payment")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    shopper_repo.update_payment(id, data.model_dump())
    return None


@router.put("/{id}/available-credit", status_code=204)
async def update_available_credit(
    id: str,
    request: Request,
    data: ShopperUpdateAvailableCreditRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update payment")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    shopper_repo.update_available_credit(id, data.model_dump())
    return None


@router.put("/{id}/payment-capacity", status_code=204)
async def update_payment_capacity(
    id: str,
    request: Request,
    data: ShopperUpdatePaymentCapacityRequest,
    auth: AuthPayload = Depends(require_permissions("User - Shopper - update payment")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    shopper_repo.update_payment_capacity(id, data.model_dump())
    return None


@router.post("/{id}/files")
async def upload_files(
    id: str,
    request: Request,
    legal_id_front: Optional[UploadFile] = File(None),
    legal_id_back: Optional[UploadFile] = File(None),
    proof_of_address: Optional[UploadFile] = File(None),
    auth: AuthPayload = Depends(require_permissions("User - Shopper - upload files")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    shopper_repo = ShopperRepository(db, cache)
    
    files_data = {}
    if legal_id_front:
        files_data['legal_id_front'] = legal_id_front
    if legal_id_back:
        files_data['legal_id_back'] = legal_id_back
    if proof_of_address:
        files_data['proof_of_address'] = proof_of_address
    
    user = shopper_repo.upload_files(id, files_data)
    
    return {
        "legal_id_front": user.profile.legal_id_front if user.profile else None,
        "legal_id_back": user.profile.legal_id_back if user.profile else None,
        "proof_of_address": user.profile.proof_of_address if user.profile else None,
    }

