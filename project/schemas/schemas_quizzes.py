from pydantic import BaseModel, validator, root_validator

from typing import Optional, List

from datetime import datetime


class Question(BaseModel):
    id: int
    question: str
    answers: list[str]
    correct_answer: str


class QuestionGet(BaseModel):
    id: int
    question: str
    answers: list[str]


class Quizz(BaseModel):
    id: int
    name: str
    description: str
    number_of_frequency: int
    quiz_questions: list[Question]
    author_id: int
    updated_by: int
    time_created: datetime
    time_updated: datetime


class Quizzes(BaseModel):
    id: int
    name: str
    description: str
    number_of_frequency: int
    author_id: int
    updated_by: int
    time_created: datetime
    time_updated: datetime


class ListQuizz(BaseModel):
    quizzes: list[Quizzes]


class CreateQuestion(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str

    @validator('answers')
    def length_of_answers(cls, v):
        if not len(v) > 2 or len(v) != len(set(v)):
            raise ValueError('There must be more than 2 answers')
        return v

    @root_validator
    def check_answer_in_answers(cls, values):
        correct_answer, answers = values.get('correct_answer'), values.get('answers')
        if correct_answer in answers:
            return values
        raise ValueError('Correct answer not in answers')


class CreateQuizz(BaseModel):
    name: str
    description: str
    number_of_frequency: int
    quiz_questions: List[CreateQuestion]

    @validator('number_of_frequency')
    def check_number_of_frequency(cls, v):
        if v <= 0:
            raise ValueError('Number of frequency must be bigger than 0')
        return v

    @validator('quiz_questions')
    def check_length_quiz_questions(cls, v):
        if len(v) <= 2:
            raise ValueError('Questions must bo more than 2')
        return v


class UpdateQuizz(BaseModel):
    name: Optional[str]
    description: Optional[str]
    number_of_frequency: Optional[int]

    @validator('number_of_frequency')
    def check_number_of_frequency(cls, v):
        if v <= 0:
            raise ValueError('Frequency must be a positive number')
        return v


class UpdateQuestion(BaseModel):
    question: Optional[str]
    answers: Optional[list[str]]
    correct_answer: Optional[str]


class QuestionComplete(BaseModel):
    id: int
    answer: str


class QuizzComplete(BaseModel):
    results: list[QuestionComplete]

    @root_validator
    def check_no_repeats(cls, values):
        results = values.get('results')
        res = []
        for item in results:
            res.append(item.id)
        if len(res) != len(set(res)):
            raise ValueError("Here must not be any repeatable question id's")
        return values


class QuizzResultComplete(BaseModel):
    id: int
    date_of_passage: datetime
    user_id: int
    company_id: int
    quizz_id: int
    general_result: float
    amount_of_questions: int
    amount_of_correct_answers: int
    avg: float
    amount_of_questions_quizz: int
    amount_of_correct_answers_quizz: int


class ShowRatingCompany(BaseModel):
    questions: int
    answers: int
    rating: float
