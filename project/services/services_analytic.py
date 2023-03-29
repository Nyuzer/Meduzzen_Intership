from databases import Database
from project.db.models import quizz_results

from datetime import datetime

from sqlalchemy import func, select

from project.schemas.schemas_quizzes import ShowRatingCompany
from project.schemas.schemas_analytics import ListQuizzesWithDynamic, QuizzWithDynamic, RecordInQuizz,\
    ListLastCompleteQuizz, LastCompleteQuizz, ListUserQuizzWithDynamic, UserQuizzWithDynamic, ListUserComplete,\
    UserComplete


class AnalyticService:
    def __init__(self, database: Database):
        self.db = database

    # rating in company
    async def get_user_general_rating_in_company(self, user_id: int, company_id: int) -> ShowRatingCompany:
        query = select(quizz_results.c.quizz_id,
                       func.max(quizz_results.c.amount_of_questions).label('amount_of_questions'),
                       func.max(quizz_results.c.amount_of_correct_answers).label('amount_of_correct_answers')) \
            .where(quizz_results.c.user_id == user_id, quizz_results.c.company_id == company_id).select_from(
            quizz_results).group_by(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        amount_questions = 0
        amount_answers = 0
        for res in result:
            amount_questions += res.amount_of_questions
            amount_answers += res.amount_of_correct_answers
        return ShowRatingCompany(questions=amount_questions, answers=amount_answers,
                                 rating=amount_answers / amount_questions)

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

    # rating in system with dynamic
    async def get_user_general_rating_with_dynamic(self, user_id: int) -> ListQuizzesWithDynamic:
        query = select(quizz_results.c.quizz_id, quizz_results.c.date_of_passage, quizz_results.c.general_result)\
            .where(quizz_results.c.user_id == user_id).select_from(quizz_results).order_by(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        query = select(quizz_results.c.quizz_id).where(quizz_results.c.user_id == user_id).select_from(quizz_results)\
            .order_by(quizz_results.c.quizz_id).distinct(quizz_results.c.quizz_id)
        ids = await self.db.fetch_all(query)
        return ListQuizzesWithDynamic(quizzes=[QuizzWithDynamic(quizz_id=item.quizz_id, result=[RecordInQuizz(
            date=record.date_of_passage, rate=record.general_result)
            for record in result if record.quizz_id == item.quizz_id]) for item in ids])

    # get last quizz
    async def get_last_complete_quizz(self, user_id: int) -> ListLastCompleteQuizz:
        query = select(quizz_results.c.quizz_id, quizz_results.c.date_of_passage)\
            .where(quizz_results.c.user_id == user_id).select_from(quizz_results)\
            .order_by(quizz_results.c.quizz_id, quizz_results.c.date_of_passage.desc())\
            .distinct(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        return ListLastCompleteQuizz(result=[LastCompleteQuizz(date=item.date_of_passage, quizz_id=item.quizz_id)
                                             for item in result])

    # get rating of all users in company
    async def get_users_quizz_dynamic(self, company_id: int) -> ListUserQuizzWithDynamic:
        query = select(quizz_results.c.user_id, quizz_results.c.date_of_passage, quizz_results.c.general_result)\
            .where(quizz_results.c.company_id == company_id).select_from(quizz_results)\
            .order_by(quizz_results.c.user_id)
        result = await self.db.fetch_all(query)
        query = select(quizz_results.c.user_id).where(quizz_results.c.company_id == company_id)\
            .select_from(quizz_results).order_by(quizz_results.c.user_id).distinct(quizz_results.c.user_id)
        ids = await self.db.fetch_all(query)
        return ListUserQuizzWithDynamic(users=[UserQuizzWithDynamic(user_id=item.user_id, result=[RecordInQuizz(
            date=record.date_of_passage, rate=record.general_result) for record in result
            if record.user_id == item.user_id]) for item in ids])

    # get rating of user in company
    async def get_member_quizz_dynamic(self, company_id: int, user_id: int) -> ListQuizzesWithDynamic:
        query = select(quizz_results.c.quizz_id, quizz_results.c.date_of_passage, quizz_results.c.general_result)\
            .where(quizz_results.c.user_id == user_id, quizz_results.c.company_id == company_id)\
            .select_from(quizz_results).order_by(quizz_results.c.quizz_id)
        result = await self.db.fetch_all(query)
        query = select(quizz_results.c.quizz_id).where(quizz_results.c.user_id == user_id,
                                                       quizz_results.c.company_id == company_id)\
            .select_from(quizz_results).order_by(quizz_results.c.quizz_id).distinct(quizz_results.c.quizz_id)
        ids = await self.db.fetch_all(query)
        return ListQuizzesWithDynamic(quizzes=[QuizzWithDynamic(quizz_id=item.quizz_id, result=[RecordInQuizz(
            date=record.date_of_passage, rate=record.general_result)
            for record in result if record.quizz_id == item.quizz_id]) for item in ids])

    # get last complete in company
    async def get_last_complete(self, company_id: int) -> ListUserComplete:
        query = select(quizz_results.c.user_id, quizz_results.c.quizz_id, quizz_results.c.date_of_passage)\
            .where(quizz_results.c.company_id == company_id).select_from(quizz_results)\
            .order_by(quizz_results.c.user_id, quizz_results.c.date_of_passage.desc()).distinct(quizz_results.c.user_id)
        result = await self.db.fetch_all(query)
        return ListUserComplete(result=[UserComplete(user_id=item.user_id, quizz_id=item.quizz_id,
                                                     date=item.date_of_passage) for item in result])
