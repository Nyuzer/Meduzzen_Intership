from pydantic import BaseModel
from typing import Optional


class Member(BaseModel):
    id: int
    user_id: int
    role: Optional[str]


class ListMember(BaseModel):
    members: list[Member]


# users requests to join company
class UserRequests(BaseModel):
    id: int
    company_id: int
    invite_message: str


class ListUserRequests(BaseModel):
    result: list[UserRequests]


class UserInvites(BaseModel):
    id: int
    company_id: int
    invite_message: str


class ListUserInvites(BaseModel):
    result: list[UserInvites]


# requests to join company
class OwnerRequests(BaseModel):
    id: int
    user_id: int
    company_id: int
    type_of_request: str


class ListOwnerRequests(BaseModel):
    result: list[OwnerRequests]


# invites to join company
class OwnerSendInvite(BaseModel):
    id: int
    user_id: int
    company_id: int
    invite_message: str


# for creation, without id
class OwnerSendInvitePost(BaseModel):
    user_id: int
    invite_message: str


class ListOwnerSendInvite(BaseModel):
    result: list[OwnerSendInvite]


class UserSendAccessionRequest(BaseModel):
    company_id: int
    invite_message: str


class ResponseSuccess(BaseModel):
    detail: str
