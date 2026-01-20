from typing import Optional, List
from pydantic import BaseModel


class AppBase(BaseModel):
    name: str
    description: Optional[str] = None


class AppCreateRequest(AppBase):
    pass


class AppUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class AppSyncPermissionsRequest(BaseModel):
    permissions: List[str] = []


class AppSyncRolesRequest(BaseModel):
    roles: List[str] = []


class AppResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: int

    class Config:
        from_attributes = True


class AppListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    order: str = "desc"
    order_column: str = "created_at"
    q: Optional[str] = None

