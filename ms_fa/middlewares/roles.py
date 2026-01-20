from typing import Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_

from ms_fa.models import Role
from ms_fa.middlewares.auth import get_current_user, AuthPayload


def require_roles(*roles: str):
    """
    Dependency factory to require specific roles.
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(auth: AuthPayload = Depends(require_roles("root", "admin"))):
            ...
    """
    async def role_checker(
        auth: AuthPayload = Depends(get_current_user)
    ) -> AuthPayload:
        user = auth.user
        
        # Root users have all access
        if user.roles.filter_by(name="root").count() > 0:
            return auth
        
        # Check if user has any of the required roles
        filters = [Role.name == role for role in roles]
        if user.roles.filter(or_(*filters)).count() > 0:
            return auth
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the required role to access this resource"
        )
    
    return role_checker

