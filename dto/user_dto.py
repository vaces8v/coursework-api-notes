from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserDB(BaseModel):
    id: int
    name: str
    last_name: str | None
    email: EmailStr
    password_hash: str
    created_at: datetime
    updated_at: datetime


class UserRegisterRequest(BaseModel):
    name: str
    last_name: str | None
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserTokenResponse(BaseModel):
    token: str
