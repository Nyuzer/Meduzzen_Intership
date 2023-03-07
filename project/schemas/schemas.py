from pydantic import BaseModel, EmailStr
from typing import Optional

from datetime import datetime


class User(BaseModel):
    id: int
    username: Optional[str] = None
    email: EmailStr
    is_root: Optional[bool]
    status: Optional[str] = None
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True


class SigninUser(BaseModel):
    email: EmailStr
    hash_password: str

    class Config:
        orm_mode = True


class SignupUser(BaseModel):
    email: EmailStr
    username: str
    hash_password: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    username: Optional[str]
    hash_password: Optional[str]
    status: Optional[str]


class ListUser(BaseModel):
    users: list[User]


class TokenResponse(BaseModel):
    token: str
