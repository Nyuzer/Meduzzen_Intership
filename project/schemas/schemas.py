from pydantic import BaseModel, EmailStr
from typing import Optional

from datetime import datetime


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_root: bool
    status: str
    time_created: datetime
    time_updated: datetime


class SigninUser(BaseModel):
    email: EmailStr
    hash_password = str


class SignupUser(SigninUser):
    pass


class UpdateUser(BaseModel):
    username: str
    email: EmailStr
    hash_password: str
    status: str


class ListUser(BaseModel):
    users: list[User]
