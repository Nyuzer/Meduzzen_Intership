from pydantic import BaseModel
from typing import Optional


class Members(BaseModel):
    id: int
    user_id: int
    role: str


class UserRequests(BaseModel):
    id: int
    company_id: int
    type_of_request: str


class OwnerRequests(BaseModel):
    id: int
    user_id: int
    type_of_request: str
