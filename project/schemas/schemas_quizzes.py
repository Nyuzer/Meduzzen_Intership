from pydantic import BaseModel, validator

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
    def length_of_answers(cls, ans: list):
        if len(ans) > 2:
            return ans
        raise ValueError('There must be more than 2 answers')

    @validator('correct_answer', 'answers')
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

    @validator('questions')
    def length_of_questions(cls, value):
        if len(value) > 2:
            return value
        raise ValueError('There must be more than 2 questions')

    class Config:
        schema_extra = {
            'examples': [
                {
                    'name': 'quizz#1',
                    'description': 'description of quizz#1',
                    'number_of_frequency': 5,
                    'questions': [
                        {
                            'question': '2+2=?',
                            'answers': ['3', '4', '7', '1'],
                            'correct_answer': '4'
                        },
                        {
                            'question': '2+3=?',
                            'answers': ['3', '4', '7', '5'],
                            'correct_answer': '5'
                        },
                        {
                            'question': '2+4=?',
                            'answers': ['3', '4', '6', '1'],
                            'correct_answer': '6'
                        }
                    ]
                }
            ]
        }


class UpdateQuizz(BaseModel):
    name: Optional[str]
    description: Optional[str]
    number_of_frequency: Optional[int]
