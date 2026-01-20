from typing import Optional
from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str


class PermissionCreateRequest(PermissionBase):
    fixed: bool = False


class PermissionUpdateRequest(BaseModel):
    name: Optional[str] = None
    fixed: Optional[bool] = None


class PermissionResponse(BaseModel):
    id: str
    name: str
    fixed: bool
    created_at: int

    class Config:
        from_attributes = True


class PermissionListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    order: str = "desc"
    order_column: str = "created_at"
    q: Optional[str] = None

