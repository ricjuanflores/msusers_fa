from typing import Optional, List
from pydantic import BaseModel

from ms_fa.schemas.permission import PermissionResponse


class RoleBase(BaseModel):
    name: str


class RoleCreateRequest(RoleBase):
    fixed: bool = False


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    fixed: Optional[bool] = None


class RoleSyncPermissionsRequest(BaseModel):
    permissions: List[str] = []


class RoleResponse(BaseModel):
    id: str
    name: str
    fixed: bool
    created_at: int

    class Config:
        from_attributes = True


class RolePermissionsResponse(RoleResponse):
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True


class RoleListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    order: str = "desc"
    order_column: str = "created_at"
    q: Optional[str] = None

