from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from ms_fa.schemas.profile import ProfileResponse, ShortProfileResponse
from ms_fa.schemas.permission import PermissionResponse
from ms_fa.schemas.role import RoleResponse


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None


class UserCreateRequest(UserBase):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    role_id: Optional[str] = None


class UserUpdateRequest(UserBase):
    pass


class UserUpdatePasswordRequest(BaseModel):
    password: str = Field(..., min_length=6)


class UserSyncPermissionsRequest(BaseModel):
    permissions: List[str] = []


class UserSyncRolesRequest(BaseModel):
    roles: List[str] = []


class UserUpdateAvailableCreditRequest(BaseModel):
    available_credit: float


class UserResponse(BaseModel):
    id: str
    aq_id: Optional[int] = None
    email: str
    phone: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None
    is_active: bool
    created_at: int
    deleted_at: Optional[int] = None
    profile: Optional[ShortProfileResponse] = None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: str
    aq_id: Optional[int] = None
    email: str
    phone: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None
    is_active: bool
    created_at: int
    deleted_at: Optional[int] = None
    profile: Optional[ProfileResponse] = None
    permissions: List[PermissionResponse] = []
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True


class UserPermissionsResponse(BaseModel):
    id: str
    aq_id: Optional[int] = None
    email: str
    phone: str
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None
    is_active: bool
    created_at: int
    deleted_at: Optional[int] = None
    permissions: List[PermissionResponse] = []
    roles: List[RoleResponse] = []

    class Config:
        from_attributes = True


class UserListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    order: str = "desc"
    order_column: str = "created_at"
    q: Optional[str] = None


class AccountUpdateRequest(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None


class AccountUpdateAuthRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class AccountUpdatePasswordRequest(BaseModel):
    password: str = Field(..., min_length=6)

