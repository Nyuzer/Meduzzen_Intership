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
    questions: list[Question]
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
            raise ValueError('There must be more than 2 answers and they must not be repeated')

    @root_validator
    def check_answer_in_answers(cls, values):
        correct_answer, answers = values.get('correct_answer'), values.get('answers')
        if correct_answer not in answers:
            raise ValueError('Here no correct answer in correct answer field')


class CreateQuizz(BaseModel):
    name: str
    description: str
    number_of_frequency: int
    questions: List[CreateQuestion]

    @validator('number_of_frequency')
    def check_number_of_frequency(cls, v):
        if v <= 0:
            raise ValueError('Frequency must be a positive number')

    @root_validator
    def length_of_questions(cls, values):
        print(values)
        value = values.get('questions')
        print(value)
        if len(value) <= 2:
            print('HEREEEEEEE')
            raise ValueError('There must be more than 2 questions')


class UpdateQuizz(BaseModel):
    name: Optional[str]
    description: Optional[str]
    number_of_frequency: Optional[int]

    @validator('number_of_frequency')
    def check_number_of_frequency(cls, v):
        if v <= 0:
            raise ValueError('Frequency must be a positive number')
