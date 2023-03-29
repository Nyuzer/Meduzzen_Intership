from databases import Database
from project.db.models import quizzes, questions, quizz_results

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from datetime import datetime

from project.schemas.schemas_quizzes import ListQuizz, CreateQuizz, UpdateQuizz, Quizzes, Quizz, Question,\
    UpdateQuestion, QuizzComplete, QuizzResultComplete, ShowRatingCompany
from project.schemas.schemas_actions import ResponseSuccess

from sqlalchemy import func, select

from project.db.connections import get_redis
from project.schemas.schemas_redis_save import RedisResultSave, RedisUserGet, ListRedisUserGet, \
    ListRedisUsersResultsGet, RedisUsersResultsGet, RedisUsersResultsByQuizzGet, ListRedisUsersResultsByQuizzGet

import json

import csv


class QuizzService:
    def __init__(self, database: Database):
        self.db = database

    @staticmethod
    def make_csv_file(result: list, pattern_name: str) -> str:
        name_file = f'project/data/{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {pattern_name}'
        data_file = open(name_file, 'w')
        csv_writer = csv.writer(data_file)
        count = 0
        for line in result:
            if count == 0:
                header = line.keys()
                csv_writer.writerow(header)
                count += 1
            values = line.values()
            csv_writer.writerow(values)
        data_file.close()
        return name_file

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

    # rating in company
    async def get_user_general_rating_in_company(self, user_id: int, company_id: int) -> ShowRatingCompany:
        query = select(quizz_results.c.quizz_id,
                       func.max(quizz_results.c.amount_of_questions).label('amount_of_questions'),
                       func.max(quizz_results.c.amount_of_correct_answers).label('amount_of_correct_answers'))\
            .where(quizz_results.c.user_id == user_id, quizz_results.c.company_id == company_id).select_from(quizz_results).group_by(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        amount_questions = 0
        amount_answers = 0
        for res in result:
            amount_questions += res.amount_of_questions
            amount_answers += res.amount_of_correct_answers
        return ShowRatingCompany(questions=amount_questions, answers=amount_answers,
                                 rating=amount_answers/amount_questions)

    # rating in system
    async def get_user_general_rating(self, user_id: int) -> ShowRatingCompany:
        query = select(quizz_results.c.quizz_id,
                       func.max(quizz_results.c.amount_of_questions).label('amount_of_questions'),
                       func.max(quizz_results.c.amount_of_correct_answers).label('amount_of_correct_answers')) \
            .where(quizz_results.c.user_id == user_id).select_from(quizz_results).group_by(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        amount_questions = 0
        amount_answers = 0
        for res in result:
            amount_questions += res.amount_of_questions
            amount_answers += res.amount_of_correct_answers
        return ShowRatingCompany(questions=amount_questions, answers=amount_answers,
                                 rating=amount_answers / amount_questions)

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

    @staticmethod
    async def get_answers_user(user_id: int) -> ListRedisUserGet:
        result = []
        redis = await get_redis()
        all_keys = await redis.keys(f's-*-{user_id}-*-*')
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            company_id = data.get('company_id')
            quizz_id = data.get('quizz_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append(RedisUserGet(company_id=company_id, quizz_id=quizz_id, question_id=question_id,
                                       answer=answer, correct=correct))
        return ListRedisUserGet(result=result)

    @staticmethod
    async def get_answers_user_csv(user_id: int) -> FileResponse:
        result = []
        redis = await get_redis()
        all_keys = await redis.keys(f's-*-{user_id}-*-*')
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            company_id = data.get('company_id')
            quizz_id = data.get('quizz_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append({'company_id': company_id, 'quizz_id': quizz_id, 'question_id': question_id,
                           'answer': answer, 'correct': correct})
        path_w_name_file = QuizzService.make_csv_file(result=result, pattern_name=f's-*-{user_id}-*-*')
        return FileResponse(path=path_w_name_file, filename=path_w_name_file)

    @staticmethod
    async def get_results_quizzes_user(company_id: int, user_id: int = 0) -> ListRedisUsersResultsGet:
        result = []
        redis = await get_redis()
        if user_id:
            all_keys = await redis.keys(f's-{company_id}-{user_id}-*-*')
        else:
            all_keys = await redis.keys(f's-{company_id}-*-*-*')
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            quizz_id = data.get('quizz_id')
            user_id = data.get('user_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append(RedisUsersResultsGet(quizz_id=quizz_id, user_id=user_id, question_id=question_id,
                                               answer=answer, correct=correct))
        return ListRedisUsersResultsGet(result=result)

    @staticmethod
    async def get_results_quizzes_user_csv(company_id: int, user_id: int = 0) -> FileResponse:
        result = []
        redis = await get_redis()
        if user_id:
            pattern = f's-{company_id}-{user_id}-*-*'
            all_keys = await redis.keys(pattern)
        else:
            pattern = f's-{company_id}-*-*-*'
            all_keys = await redis.keys(pattern)
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            quizz_id = data.get('quizz_id')
            user_id = data.get('user_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append({'quizz_id': quizz_id, 'user_id': user_id, 'question_id': question_id, 'answer': answer,
                           'correct': correct})
        path_w_name_file = QuizzService.make_csv_file(result=result, pattern_name=pattern)
        return FileResponse(path=path_w_name_file, filename=path_w_name_file)

    @staticmethod
    async def get_by_quizz_results(company_id: int, quizz_id: int) -> ListRedisUsersResultsByQuizzGet:
        result = []
        redis = await get_redis()
        all_keys = await redis.keys(f's-{company_id}-*-{quizz_id}-*')
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            user_id = data.get('user_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append(RedisUsersResultsByQuizzGet(user_id=user_id, question_id=question_id,
                                                      answer=answer, correct=correct))
        return ListRedisUsersResultsByQuizzGet(result=result)

    @staticmethod
    async def get_by_quizz_results_csv(company_id: int, quizz_id: int) -> FileResponse:
        result = []
        redis = await get_redis()
        all_keys = await redis.keys(f's-{company_id}-*-{quizz_id}-*')
        for key in all_keys:
            value = await redis.get(key)
            data = eval(value.replace('true', 'True').replace('false', 'False'))
            user_id = data.get('user_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            correct = data.get('correct')
            result.append({'user_id': user_id, 'question_id': question_id, 'answer': answer, 'correct': correct})
        path_w_name_file = QuizzService.make_csv_file(result=result, pattern_name=f's-{company_id}-*-{quizz_id}-*')
        return FileResponse(path=path_w_name_file, filename=path_w_name_file)

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

    async def quizz_complete(self, quizz_id: int, company_id: int, user_id: int,
                             results: QuizzComplete) -> QuizzResultComplete:
        query = questions.select().where(questions.c.quizz_id == quizz_id)
        all_questions = await self.db.fetch_all(query)
        all_questions = {item.id: item.correct_answer for item in all_questions}
        result = {
            'amount_of_questions_quizz': len(all_questions),
            'amount_of_correct_answers_quizz': 0
        }
        redis = await get_redis()
        for ques in results.results:
            if all_questions.get(ques.id) is None:
                continue
            if all_questions.get(ques.id) == ques.answer:
                result['amount_of_correct_answers_quizz'] += 1
                correct = True
            else:
                correct = False
            value_in_redis = RedisResultSave(
                user_id=user_id, company_id=company_id, quizz_id=quizz_id, question_id=ques.id, answer=ques.answer,
                correct=correct
            )
            await redis.set(f's-{company_id}-{user_id}-{quizz_id}-{ques.id}',
                            json.dumps(dict(value_in_redis)), ex=172800)
        result['avg'] = result['amount_of_correct_answers_quizz'] / result['amount_of_questions_quizz']
        query = quizz_results.select().where(quizz_results.c.user_id == user_id, quizz_results.c.quizz_id == quizz_id)\
            .order_by(quizz_results.c.date_of_passage.desc())
        last_record = await self.db.fetch_one(query)
        if last_record is not None:
            result['amount_of_questions'] = last_record.amount_of_questions + result['amount_of_questions_quizz']
            result['amount_of_correct_answers'] =\
                last_record.amount_of_correct_answers + result['amount_of_correct_answers_quizz']
        else:
            result['amount_of_questions'] = result['amount_of_questions_quizz']
            result['amount_of_correct_answers'] = result['amount_of_correct_answers_quizz']
        result['general_result'] = result['amount_of_correct_answers'] / result['amount_of_questions']
        query = quizz_results.insert().values(date_of_passage=datetime.utcnow(), user_id=user_id, company_id=company_id,
                                              quizz_id=quizz_id, general_result=result['general_result'],
                                              amount_of_questions=result['amount_of_questions'],
                                              amount_of_correct_answers=result['amount_of_correct_answers'],
                                              avg=result['avg'],
                                              amount_of_questions_quizz=result['amount_of_questions_quizz'],
                                              amount_of_correct_answers_quizz=result['amount_of_correct_answers_quizz'])
        pk = await self.db.execute(query)
        return QuizzResultComplete(id=pk, date_of_passage=datetime.utcnow(), user_id=user_id, company_id=company_id,
                                   quizz_id=quizz_id, general_result=result['general_result'],
                                   amount_of_questions=result['amount_of_questions'],
                                   amount_of_correct_answers=result['amount_of_correct_answers'],
                                   avg=result['avg'],
                                   amount_of_questions_quizz=result['amount_of_questions_quizz'],
                                   amount_of_correct_answers_quizz=result['amount_of_correct_answers_quizz'])


"""
{
  "results": [
    {
      "id": 1,
      "answer": "4"
    },
    {
      "id": 15,
      "answer": "5"
    },
    {
      "id": 102,
      "answer": "9"
    },
    {
      "id": 2,
      "answer": "5"
    },
    {
      "id": 3,
      "answer": "4"
    }
  ]
}
"""
