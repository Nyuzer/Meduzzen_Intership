from pydantic import BaseModel

from datetime import datetime


class HiddenNotification(BaseModel):
    id: int
    status: str
    received: datetime


class ListHiddenNotification(BaseModel):
    result: list[HiddenNotification]


class Notification(BaseModel):
    id: int
    received: datetime
    status: str
    message: str
