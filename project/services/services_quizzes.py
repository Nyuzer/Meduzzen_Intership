from databases import Database
from project.db.models import quizzes, questions

from fastapi import HTTPException, status

from datetime import datetime

from project.schemas.schemas_quizzes import ListQuizz, CreateQuizz, UpdateQuizz, Quizzes, Quizz, Question,\
    UpdateQuestion
from project.schemas.schemas_actions import ResponseSuccess


class QuizzService:
    def __init__(self, database: Database):
        self.db = database

    @staticmethod
    def check_length_answers(answers: list) -> bool:
        if len(answers) > 2:
            return True
        return False

    @staticmethod
    def check_correct_answer_in_answers(correct_answer: str, answers: list) -> bool:
        if correct_answer in answers:
            return True
        return False

    async def your_company_quizz(self, quizz_id: int, company_id: int) -> bool:
        query = quizzes.select().where(quizzes.c.id == quizz_id)
        quizz_company = await self.db.fetch_one(query)
        return quizz_company.company_id == company_id

    async def question_related_to_quizz(self, quizz_id: int, question_id: int) -> bool:
        query = questions.select().where(questions.c.id == question_id)
        question_quizz = await self.db.fetch_one(query)
        return question_quizz.quizz_id == quizz_id

    async def check_exist_quizz(self, quizz_id: int) -> bool:
        query = quizzes.select().where(quizzes.c.id == quizz_id)
        item = await self.db.fetch_one(query)
        return item is not None

    async def check_exists_question(self, question_id: int) -> bool:
        query = questions.select().where(questions.c.id == question_id)
        item = await self.db.fetch_one(query)
        return item is not None

    async def check_exist_quizz_by_name(self, quizz_name: str) -> bool:
        query = quizzes.select().where(quizzes.c.name == quizz_name)
        item = await self.db.fetch_one(query)
        return item is not None

    async def get_quizzes(self, company_id: int) -> ListQuizz:
        query = quizzes.select().where(quizzes.c.company_id == company_id)
        items = await self.db.fetch_all(query)
        return ListQuizz(quizzes=[Quizzes(id=item.id, name=item.name, description=item.description,
                                          number_of_frequency=item.number_of_frequency, author_id=item.author_id,
                                          updated_by=item.updated_by, time_created=item.time_created,
                                          time_updated=item.time_updated) for item in items])

    async def quizz_get_by_id(self, quizz_id: int) -> Quizz:
        query = quizzes.select().where(quizzes.c.id == quizz_id)
        quizz = await self.db.fetch_one(query)
        query = questions.select().where(questions.c.quizz_id == quizz_id)
        quests = await self.db.fetch_all(query)
        return Quizz(id=quizz.id, name=quizz.name, description=quizz.description,
                     number_of_frequency=quizz.number_of_frequency, quiz_questions=[Question(id=item.id,
                                                                                             question=item.question,
                                                                                             answers=item.answers,
                                                                                             correct_answer=item.correct_answer)
                                                                                    for item in quests],
                     author_id=quizz.author_id, updated_by=quizz.updated_by, time_created=quizz.time_created,
                     time_updated=quizz.time_updated)

    async def quizz_create(self, quizz: CreateQuizz, company_id: int, author_id: int) -> ResponseSuccess:
        query = quizzes.insert().values(name=quizz.name, description=quizz.description,
                                        number_of_frequency=quizz.number_of_frequency, author_id=author_id,
                                        updated_by=author_id, company_id=company_id, time_created=datetime.utcnow(),
                                        time_updated=datetime.utcnow())
        pk = await self.db.execute(query)
        result = []
        for item in quizz.quiz_questions:
            result.append({"question": item.question, "answers": item.answers,
                           "correct_answer": item.correct_answer, "quizz_id": pk})
        query = questions.insert().values(result)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def quizz_update(self, quizz_id: int, quizz: UpdateQuizz, updated_by: int) -> ResponseSuccess:
        updated = {k: v for k, v in quizz.dict().items() if v is not None}
        query = quizzes.update().where(quizzes.c.id == quizz_id).values(**updated, updated_by=updated_by)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    @staticmethod
    async def update_question(db: Database, values: dict, user_id: int, question_id: int,
                              quizz_id: int) -> ResponseSuccess:
        query = questions.update().where(questions.c.id == question_id).values(**values)
        await db.execute(query)
        query = quizzes.update().where(quizzes.c.id == quizz_id).values(updated_by=user_id)
        await db.execute(query)
        return ResponseSuccess(detail='success')

    async def validate_question(self, database: Database, question: UpdateQuestion, question_id: int,
                                user_id: int, quizz_id: int) -> ResponseSuccess:
        values = {}
        if question.question:
            values['question'] = question.question
        if question.answers:
            if QuizzService.check_length_answers(answers=question.answers):
                if question.correct_answer:
                    result = QuizzService.check_correct_answer_in_answers(correct_answer=question.correct_answer,
                                                                          answers=question.answers)
                    if result:
                        values['answers'] = question.answers
                        values['correct_answer'] = question.correct_answer
                    else:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail='Correct answer should be in answers')
                else:
                    query = questions.select().where(questions.c.id == question_id)
                    question_old = await self.db.fetch_one(query)
                    result = QuizzService.check_correct_answer_in_answers(correct_answer=question_old.correct_answer,
                                                                          answers=question.answers)
                    if result:
                        values['answers'] = question.answers
                    else:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail='Correct answer should be in answers')
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail='Answers should be more than two')
        elif question.correct_answer:
            query = questions.select().where(questions.c.id == question_id)
            question_old = await self.db.fetch_one(query)
            result = QuizzService.check_correct_answer_in_answers(correct_answer=question.correct_answer,
                                                                  answers=question_old.answers)
            if result:
                values['correct_answer'] = question.correct_answer
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail='Correct answer should be in answers')
        return await QuizzService.update_question(db=database, values=values, user_id=user_id, question_id=question_id,
                                                  quizz_id=quizz_id)

    async def quizz_delete(self, quizz_id: int) -> ResponseSuccess:
        query = quizzes.delete().where(quizzes.c.id == quizz_id)
        await self.db.execute(query)
        query = questions.delete().where(questions.c.quizz_id == quizz_id)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')


# for future ->
"""return ListQuizz(result=[QuizzSchema(id=quiz.quizzes.id, name=quiz.quizzes.name,
                                             description=quiz.quizzes.description,
                                             number_of_frequency=quiz.quizzes.number_of_frequency,
                                             questions=[QuestionGet(id=item.questions.id,
                                                                    question=item.questions.question,
                                                                    answers=item.questions.answers)
                                                        for item in items if quiz.quizzes.id == item.questions.quizz_id]
                                             , time_created=quiz.quizzes.time_created,
                                             time_updated=quiz.quizzes.time_updated) for quiz in items])"""
