from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class PersonalReferenceSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None


class ProfileBase(BaseModel):
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
    personal_references: Optional[List[PersonalReferenceSchema]] = None


class ProfileUpdateRequest(ProfileBase):
    pass


class ProfilePatchRequest(ProfileBase):
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None


class ProfileResponse(ProfileBase):
    entity_birth_name: Optional[str] = None
    state_name: Optional[str] = None
    available_credit: Optional[float] = None
    pay_id: Optional[str] = None
    payment_capacity: Optional[float] = None
    second_credit: Optional[bool] = None
    kyc_prescoring_id: Optional[int] = None
    legal_id_front: Optional[str] = None
    legal_id_back: Optional[str] = None
    proof_of_address: Optional[str] = None

    class Config:
        from_attributes = True


class ShortProfileResponse(BaseModel):
    rfc: Optional[str] = None
    curp: Optional[str] = None

    class Config:
        from_attributes = True


class ShopperFilesResponse(BaseModel):
    legal_id_front: Optional[str] = None
    legal_id_back: Optional[str] = None
    proof_of_address: Optional[str] = None

    class Config:
        from_attributes = True

