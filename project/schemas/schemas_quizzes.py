from pydantic import BaseModel, validator, root_validator

from typing import Optional

from datetime import datetime


class Question(BaseModel):
    id: int
    question: str
    answers: list[str]
    correct_answer: str


class Quizz(BaseModel):
    id: int
    name: str
    description: str
    number_of_frequency: int
    questions: list[Question]
    time_created: datetime
    time_updated: datetime


class ListQuizz(BaseModel):
    quizzes: list[Quizz]


class CreateQuestion(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str

    @validator('answers')
    def length_of_answers(cls, v):
        if len(v) > 2:
            return v
        raise ValueError('There must be more than 2 answers')

    # @validator('answers', 'correct_answer')
    @root_validator
    def check_answer_in_answers(cls, values):
        correct_answer, answers = values.get('correct_answer'), values.get('answers')
        if correct_answer in answers:
            return answers
        raise ValueError('Here no correct answer in correct answer field')


class CreateQuizz(BaseModel):
    name: str
    description: str
    number_of_frequency: int
    questions: list[CreateQuestion]

    @root_validator
    def length_of_questions(cls, values):
        print('@!!!@!&^&&^@#^@*&^&#@&*^#@&*#@&*#@*@#@#*')
        print(values)
        value = values.get('questions')
        print(value)
        if len(value) > 2:
            print('HEREEEEEEE')
            return value
        print('WRONGGGG')
        raise ValueError('There must be more than 2 questions')


class UpdateQuizz(BaseModel):
    name: Optional[str]
    description: Optional[str]
    number_of_frequency: Optional[int]
