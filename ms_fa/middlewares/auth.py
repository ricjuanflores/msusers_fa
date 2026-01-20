from typing import Optional, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ms_fa.db import get_db
from ms_fa.helpers.jwt import JwtHelper
from ms_fa.repositories import UserRepository, AppRepository


security = HTTPBearer()


class AuthPayload(BaseModel):
    id: str
    aq_id: Optional[int] = None
    session: Optional[str] = None
    exp: int
    user: Any = None

    class Config:
        arbitrary_types_allowed = True


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AuthPayload:
    """
    Dependency to get the current authenticated user from JWT token.
    """
    token = credentials.credentials
    jwt_helper = JwtHelper()
    
    # Validate token
    if not jwt_helper.check(f"Bearer {token}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Decode token
    try:
        payload = jwt_helper.decode(f"Bearer {token}")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get cache from app state
    cache = getattr(request.app.state, 'cache', None)
    
    # Find user or app
    user_repo = UserRepository(db, cache)
    app_repo = AppRepository(db, cache)
    
    entity = user_repo.find(payload.get('id'), fail=False)
    
    if not entity:
        entity = app_repo.find(payload.get('id'), fail=False)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    auth_payload = AuthPayload(
        id=payload.get('id'),
        aq_id=payload.get('aq_id'),
        session=payload.get('session'),
        exp=payload.get('exp'),
        user=entity
    )
    
    return auth_payload


def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[AuthPayload]:
    """
    Optional dependency to get the current authenticated user.
    Returns None if no valid token is provided.
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(request, credentials, db)
    except HTTPException:
        return None

