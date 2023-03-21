from databases import Database
from project.db.models import quizzes, questions

from datetime import datetime

from project.schemas.schemas_quizzes import Quizz, Question, ListQuizz, CreateQuizz, UpdateQuizz
from project.schemas.schemas_actions import ResponseSuccess


class QuizzService:
    def __init__(self, database: Database):
        self.db = database

    async def check_exist_quizz(self, quizz_id: int) -> bool:
        query = quizzes.select().where(quizzes.c.id == quizz_id)
        item = await self.db.fetch_one(query)
        return item is not None

    async def get_quizzes(self, company_id: int) -> ListQuizz:
        # join table что бы было две таблицы в селекте
        # query = quizz
        query = quizzes.select().where(quizzes.c.company_id == company_id)
        items = await self.db.execute(query)
        # что то похожее на это
        return ListQuizz(result=[Quizz(id=quiz.quizzes.id, name=quiz.quizzes.name,
                                       description=quiz.quizzes.description,
                                       number_of_frequency=quiz.quizzes.number_of_frequency,
                                       questions=[Question(id=item.questions.id, question=item.questions.question,
                                                           answers=item.questions.answers.split('|'),
                                                           correct_answer=item.questions.correct_answer)
                                                  for item in items if quiz.quizzes.id == item.questions.quizz_id],
                                       time_created=quiz.quizzes.time_created,
                                       time_updated=quiz.quizzes.time_updated
                                       ) for quiz in items])

    # how to decode 'a|b' -> string_from_db.split('|')
    async def quizz_create(self, quizz: CreateQuizz, company_id: int, author_id: int) -> ResponseSuccess:
        query = quizzes.insert().values(name=quizz.name, description=quizz.description,
                                        number_of_frequency=quizz.number_of_frequency, author_id=author_id,
                                        company_id=company_id, time_created=datetime.utcnow(),
                                        time_updated=datetime.utcnow())
        pk = await self.db.execute(query)
        for item in quizz.questions:
            item.answers = '|'.join(item.answers)
            query = questions.insert().values(question=item.question, answers=item.answers,
                                              correct_answer=item.correct_answer, quizz_id=pk)
            await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def quizz_update(self, quizz_id: int, quizz: UpdateQuizz) -> ResponseSuccess:
        updated = {k: v for k, v in quizz.dict().items() if v is not None}
        query = quizzes.update().where(quizzes.c.id == quizz_id).values(**updated)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def quizz_delete(self, quizz_id: int) -> ResponseSuccess:
        query = quizzes.delete().where(quizzes.c.id == quizz_id)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')
