from pydantic import BaseModel


class RedisResultSave(BaseModel):
    user_id: int
    company_id: int
    quizz_id: int
    question_id: int
    answer: str
    correct: bool


class RedisUserGet(BaseModel):
    company_id: int
    quizz_id: int
    question_id: int
    answer: str
    correct: bool


class ListRedisUserGet(BaseModel):
    result: list[RedisUserGet]


class RedisUsersResultsGet(BaseModel):
    quizz_id: int
    user_id: int
    question_id: int
    answer: str
    correct: bool


class ListRedisUsersResultsGet(BaseModel):
    result: list[RedisUsersResultsGet]


class RedisUsersResultsByQuizzGet(BaseModel):
    user_id: int
    question_id: int
    answer: str
    correct: bool


class ListRedisUsersResultsByQuizzGet(BaseModel):
    result: list[RedisUsersResultsByQuizzGet]
