from pydantic import BaseModel
from typing import Optional


class Member(BaseModel):
    id: int
    user_id: int
    role: Optional[str]


class ListMember(BaseModel):
    members: list[Member]


class UserRequests(BaseModel):
    id: int
    company_id: int
    type_of_request: str


class OwnerRequests(BaseModel):
    id: int
    user_id: int
    company_id: int
    type_of_request: str


class ListOwnerRequests(BaseModel):
    result: list[OwnerRequests]


class OwnerSendInvite(BaseModel):
    id: int
    user_id: int
    company_id: int
    invite_message: str


class ListOwnerSendInvite(BaseModel):
    result: list[OwnerSendInvite]


class UserSendAccessionRequest(BaseModel):
    company_id: int
