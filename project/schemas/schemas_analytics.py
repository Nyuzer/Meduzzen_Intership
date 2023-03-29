from pydantic import BaseModel

from datetime import datetime


class RecordInQuizz(BaseModel):
    date: datetime
    rate: float


class QuizzWithDynamic(BaseModel):
    quizz_id: int
    result: list[RecordInQuizz]


class ListQuizzesWithDynamic(BaseModel):
    quizzes: list[QuizzWithDynamic]


class LastCompleteQuizz(BaseModel):
    date: datetime
    quizz_id: int


class ListLastCompleteQuizz(BaseModel):
    result: list[LastCompleteQuizz]


class UserQuizzWithDynamic(BaseModel):
    user_id: int
    result: list[RecordInQuizz]


class ListUserQuizzWithDynamic(BaseModel):
    users: list[UserQuizzWithDynamic]


class UserComplete(BaseModel):
    user_id: int
    quizz_id: int
    date: datetime


class ListUserComplete(BaseModel):
    result: list[UserComplete]
