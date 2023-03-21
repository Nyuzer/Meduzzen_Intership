from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class Company(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class CompanyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class ListCompany(BaseModel):
    companies: list[Company]


