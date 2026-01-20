import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ms_fa.db import get_db
from ms_fa.helpers.jwt import JwtHelper
from ms_fa.helpers.time import epoch_now
from ms_fa.helpers.utils import random_integer, random_string
from ms_fa.helpers.notification import send_reset_password_notification
from ms_fa.middlewares import get_current_user, AuthPayload, require_permissions
from ms_fa.repositories import UserRepository, ShopperRepository, ResetPasswordRepository, SessionRepository
from ms_fa.schemas.auth import (
    AuthRegisterRequest,
    AuthLoginRequest,
    AuthGenerateTokenRequest,
    AuthValidateEmailRequest,
    AuthForgotPasswordRequest,
    AuthResetPasswordRequest,
    ValidateTokenNotificationRequest,
    AuthTokenResponse,
    AuthValidateEmailResponse,
    ForgotPasswordResponse,
)
from ms_fa.schemas.user import UserProfileResponse

router = APIRouter()


def get_token(user, jwt_helper: JwtHelper):
    data = {
        "id": user.id,
        "aq_id": user.aq_id,
        "session": random_string(length=64),
        "available_credit": user.profile.available_credit if user.profile else 0,
        "payment_capacity": user.profile.payment_capacity if user.profile else 0,
        "second_credit": user.profile.second_credit if user.profile else False,
        "roles": [role.name for role in user.roles],
    }
    return jwt_helper.get_tokens(data), data


def save_login_data(user, payload, session_repo: SessionRepository, user_repo: UserRepository, jwt_helper: JwtHelper, cache=None):
    session_repo.add({
        "user_id": user.id,
        "token": payload.get("session", ""),
        "expires_at": datetime.datetime.fromtimestamp(epoch_now() + jwt_helper.token_lifetime),
    })
    if cache:
        user_repo.cache = cache
    user_repo.setCache(user, force=True)


@router.post("/register", response_model=AuthTokenResponse, status_code=201)
async def register(
    request: Request,
    data: AuthRegisterRequest,
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=60*60*24*15, refresh_token_lifetime=60*60*24*20)
    shopper_repo = ShopperRepository(db, cache)
    user_repo = UserRepository(db, cache)
    session_repo = SessionRepository(db)
    
    user = shopper_repo.add(data.model_dump())
    token, payload = get_token(user, jwt_helper)
    save_login_data(user, payload, session_repo, user_repo, jwt_helper, cache)
    
    return token


@router.post("/login", response_model=AuthTokenResponse)
async def login(
    request: Request,
    data: AuthLoginRequest,
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=60*60*24*15, refresh_token_lifetime=60*60*24*20)
    user_repo = UserRepository(db, cache)
    session_repo = SessionRepository(db)
    
    user = user_repo.find_optional({"phone": data.username, "email": data.username}, fail=False)
    
    if user is None or not user.verify_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The credentials do not match our records."
        )
    
    token, payload = get_token(user, jwt_helper)
    save_login_data(user, payload, session_repo, user_repo, jwt_helper, cache)
    
    return token


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    user_repo = UserRepository(db, cache)
    session_repo = SessionRepository(db)
    
    session_repo.delete(auth.user, auth.session)
    
    if not session_repo.has_active_session(auth.user):
        user_repo.deleteCache(auth.user)
    
    return None


@router.post("/refresh", response_model=AuthTokenResponse)
async def refresh_token(
    request: Request,
    auth: AuthPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=60*60*24*15, refresh_token_lifetime=60*60*24*20)
    user_repo = UserRepository(db, cache)
    session_repo = SessionRepository(db)
    
    token, payload = get_token(auth.user, jwt_helper)
    save_login_data(auth.user, payload, session_repo, user_repo, jwt_helper, cache)
    
    return token


@router.post("/generate-token", response_model=AuthTokenResponse)
async def generate_token(
    request: Request,
    data: AuthGenerateTokenRequest,
    auth: AuthPayload = Depends(require_permissions("User - generate token")),
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=60*60*24*15, refresh_token_lifetime=60*60*24*20)
    user_repo = UserRepository(db, cache)
    session_repo = SessionRepository(db)
    
    user = user_repo.find_by_phone_and_email(data.phone, data.email)
    token, payload = get_token(user, jwt_helper)
    save_login_data(user, payload, session_repo, user_repo, jwt_helper, cache)
    
    return token


@router.post("/check", status_code=204)
async def check(auth: AuthPayload = Depends(get_current_user)):
    return None


@router.post("/validate-email")
async def validate_email(
    data: AuthValidateEmailRequest,
    auth: AuthPayload = Depends(require_permissions("User - validate email")),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.find_optional({"phone": data.username, "email": data.username}, fail=False)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "name": user.name,
        "lastname": user.lastname,
    }


@router.post("/validate-token-notification", status_code=204)
async def validate_token_notification(
    data: ValidateTokenNotificationRequest,
    db: Session = Depends(get_db)
):
    reset_repo = ResetPasswordRepository(db)
    token = reset_repo.get_by_token_and_username(data.token, data.username, fail=False)
    
    if token is None or token.expires_at < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": {"token": ["The token is invalid."]}}
        )
    
    return None


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    data: AuthForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    reset_repo = ResetPasswordRepository(db)
    
    user = user_repo.find_optional({"phone": data.username, "email": data.username}, fail=False)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": {"username": ["El número de whatsapp o correo electronico no ha sido registrado."]}}
        )
    
    random_number = random_integer(6)
    reset_repo.add({
        "username": data.username,
        "token": random_number,
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
    })
    
    send_reset_password_notification(user.phone, random_number)
    
    return {"phone": f"{'*' * 6}{user.phone[6:]}"}


@router.post("/reset-password", response_model=AuthTokenResponse)
async def reset_password(
    request: Request,
    data: AuthResetPasswordRequest,
    db: Session = Depends(get_db)
):
    cache = getattr(request.app.state, 'cache', None)
    jwt_helper = JwtHelper(token_lifetime=60*60*24*15, refresh_token_lifetime=60*60*24*20)
    user_repo = UserRepository(db, cache)
    reset_repo = ResetPasswordRepository(db)
    session_repo = SessionRepository(db)
    
    token_obj = reset_repo.get_by_token(data.token, fail=False)
    
    if token_obj is None or token_obj.expires_at < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": {"token": ["The token is invalid."]}}
        )
    
    user = user_repo.find_optional({"phone": token_obj.username, "email": token_obj.username}, fail=False)
    reset_repo.delete(token_obj.id)
    user_repo.update_password(user, data.password)
    
    token, payload = get_token(user, jwt_helper)
    save_login_data(user, payload, session_repo, user_repo, jwt_helper, cache)
    
    return token

