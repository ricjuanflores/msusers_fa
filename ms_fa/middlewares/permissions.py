from typing import Tuple
from fastapi import Depends, HTTPException, status

from ms_fa.middlewares.auth import get_current_user, AuthPayload


def require_permissions(*permissions: str):
    """
    Dependency factory to require specific permissions.
    
    Usage:
        @router.get("/endpoint")
        async def endpoint(auth: AuthPayload = Depends(require_permissions("User - list", "User - detail"))):
            ...
    """
    async def permission_checker(
        auth: AuthPayload = Depends(get_current_user)
    ) -> AuthPayload:
        user = auth.user
        
        # Root users have all permissions
        if user.roles.filter_by(name="root").count() > 0:
            return auth
        
        # Check if user has any of the required permissions
        user_permissions = [p.name for p in user.all_permissions]
        for permission in permissions:
            if permission in user_permissions:
                return auth
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
    
    return permission_checker

