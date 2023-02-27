from pydantic import BaseModel, EmailStr
from typing import Optional

from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr
    hash_password: str


class SigninUser(BaseModel):
    email: EmailStr
    hash_password = str


class SignupUser(User):
    pass


class UpdateUser(User):
    pass


class ListUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_root: bool
    time_created: datetime
    time_updated: datetime
