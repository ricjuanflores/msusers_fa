from typing import Optional, List, Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class PaginationMeta(BaseModel):
    page: int
    pages: int
    per_page: int
    prev: Optional[int] = None
    next: Optional[int] = None
    total: int


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: PaginationMeta


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    message: str
    name: Optional[str] = None
    status: int


class ValidationErrorResponse(BaseModel):
    errors: dict

