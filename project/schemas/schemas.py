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
    email: Optional[EmailStr]
    hash_password: Optional[str]

    class Config:
        orm_mode = True


class SignupUser(BaseModel):
    email: Optional[EmailStr]
    hash_password: Optional[str]

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    hash_password: Optional[str]
    status: Optional[str]


class ListUser(BaseModel):
    users: list[User]
