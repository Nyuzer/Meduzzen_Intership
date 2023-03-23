from databases import Database
from project.db.models import quizzes, questions
from sqlalchemy import select

from datetime import datetime

from project.schemas.schemas_quizzes import ListQuizz, CreateQuizz, UpdateQuizz, Quizzes, Quizz, Question
from project.schemas.schemas_actions import ResponseSuccess


class QuizzService:
    def __init__(self, database: Database):
        self.db = database

    async def check_exist_quizz(self, quizz_id: int) -> bool:
        query = quizzes.select().where(quizzes.c.id == quizz_id)
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
