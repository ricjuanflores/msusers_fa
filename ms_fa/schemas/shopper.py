from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class ShopperCreateRequest(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None


class ShopperUpdateRequest(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None
    rfc: Optional[str] = None
    curp: Optional[str] = None
    home_phone: Optional[str] = None
    birthday: Optional[str] = None
    entity_birth: Optional[str] = None
    gender: Optional[str] = None
    grade: Optional[str] = None
    marital_status: Optional[str] = None
    municipality: Optional[str] = None
    street: Optional[str] = None
    reference_street: Optional[str] = None
    reference_street_other: Optional[str] = None
    additional_reference: Optional[str] = None
    exterior: Optional[str] = None
    interior: Optional[str] = None
    neighborhood: Optional[str] = None
    zip: Optional[str] = None
    department: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    monthly_expenditure: Optional[float] = None
    income: Optional[float] = None
    income_family: Optional[float] = None
    count_home: Optional[int] = None
    count_income_people: Optional[int] = None
    company_name: Optional[str] = None
    type_activity: Optional[str] = None
    position: Optional[str] = None
    time_activity_year: Optional[int] = None
    time_activity_month: Optional[int] = None


class ShopperPatchRequest(ShopperUpdateRequest):
    pass


class ShopperUpdateSecondCreditRequest(BaseModel):
    second_credit: bool


class ShopperUpdateKycPrescoringRequest(BaseModel):
    prescoring_id: int


class ShopperUpdatePaymentRequest(BaseModel):
    available_credit: float = 0
    payment_capacity: float = 0


class ShopperUpdateAvailableCreditRequest(BaseModel):
    available_credit: float


class ShopperUpdatePaymentCapacityRequest(BaseModel):
    payment_capacity: float


class ShopperUpdatePayIdRequest(BaseModel):
    pay_id: str


class ShopperListParams(BaseModel):
    page: int = 1
    per_page: int = 15
    search: Optional[str] = None

