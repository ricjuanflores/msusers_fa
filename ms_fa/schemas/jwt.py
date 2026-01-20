from typing import Optional, List
from pydantic import BaseModel


class JwtPayload(BaseModel):
    id: str
    aq_id: Optional[int] = None
    session: str
    roles: List[str] = []
    available_credit: Optional[float] = 0
    payment_capacity: Optional[float] = 0
    second_credit: Optional[bool] = False


class AppJwtPayload(BaseModel):
    id: str

