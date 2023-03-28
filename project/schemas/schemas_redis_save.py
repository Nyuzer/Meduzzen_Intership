from pydantic import BaseModel


class RedisResultSave(BaseModel):
    user_id: int
    company_id: int
    quizz_id: int
    question_id: int
    answer: str
    correct: bool
