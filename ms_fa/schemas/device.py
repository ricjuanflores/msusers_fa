from typing import Optional
from pydantic import BaseModel


class DeviceBase(BaseModel):
    device_id: Optional[str] = None
    mark: Optional[str] = None
    model: Optional[str] = None
    carrier: Optional[str] = None
    os: Optional[str] = None
    nfc: Optional[bool] = False
    app_version: Optional[str] = None


class DeviceCreateRequest(DeviceBase):
    user_id: Optional[str] = None


class DeviceUpdateRequest(DeviceBase):
    pass


class DeviceResponse(BaseModel):
    id: str
    device_id: Optional[str] = None
    mark: Optional[str] = None
    model: Optional[str] = None
    carrier: Optional[str] = None
    os: Optional[str] = None
    nfc: Optional[bool] = None
    app_version: Optional[str] = None
    created_at: int

    class Config:
        from_attributes = True


class DeviceUserResponse(DeviceResponse):
    user_id: Optional[str] = None

    class Config:
        from_attributes = True


class DeviceListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    order: str = "desc"
    order_column: str = "created_at"
    q: Optional[str] = None

