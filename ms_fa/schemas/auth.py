from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class AuthRegisterRequest(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    name: Optional[str] = None
    lastname: Optional[str] = None
    second_lastname: Optional[str] = None


class AuthLoginRequest(BaseModel):
    username: str = Field(..., description="Email or phone number")
    password: str = Field(..., min_length=1)


class AuthGenerateTokenRequest(BaseModel):
    phone: str
    email: EmailStr


class AuthValidateEmailRequest(BaseModel):
    username: str


class AuthForgotPasswordRequest(BaseModel):
    username: str


class AuthResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(..., min_length=6)


class ValidateTokenNotificationRequest(BaseModel):
    username: str
    token: str


class AuthTokenResponse(BaseModel):
    token: str
    refresh_token: str


class AuthValidateEmailResponse(BaseModel):
    id: str
    email: str
    phone: str
    name: Optional[str] = None
    lastname: Optional[str] = None


class ForgotPasswordResponse(BaseModel):
    phone: str

