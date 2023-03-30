from fastapi import APIRouter, HTTPException, status, Depends

from databases import Database

from project.services.services import get_current_user

from project.db.connections import get_db

from project.schemas.schemas import User
from project.schemas.schemas_quizzes import ShowRatingCompany
from project.schemas.schemas_analytics import ListQuizzesWithDynamic, ListLastCompleteQuizz, ListUserQuizzWithDynamic,\
    ListUserComplete

from project.services.services_company import CompanyService
from project.services.services_actions import ActionsService
from project.services.services_analytic import AnalyticService


router = APIRouter()


@router.get('/my/general', status_code=200, response_model=ShowRatingCompany)
async def get_rating_general(db: Database = Depends(get_db),
                             user: User = Depends(get_current_user)) -> ShowRatingCompany:
    analytics = AnalyticService(database=db)
    return await analytics.get_user_general_rating(user_id=user.id)


@router.get('/my/general/dynamic', status_code=200, response_model=ListQuizzesWithDynamic)
async def get_rating_general_dynamic(db: Database = Depends(get_db),
                                     user: User = Depends(get_current_user)) -> ListQuizzesWithDynamic:
    analytics = AnalyticService(database=db)
    return await analytics.get_user_general_rating_with_dynamic(user_id=user.id)


@router.get('/my/last/quizzes', status_code=200, response_model=ListLastCompleteQuizz)
async def get_last_quizz(db: Database = Depends(get_db),
                         user: User = Depends(get_current_user)) -> ListLastCompleteQuizz:
    analytics = AnalyticService(database=db)
    return await analytics.get_last_complete_quizz(user_id=user.id)


@router.get('/{company_id}/general/dynamic', status_code=200, response_model=ListUserQuizzWithDynamic)
async def get_general_rating_all_members(company_id: int, db: Database = Depends(get_db),
                                         user: User = Depends(get_current_user)) -> ListUserQuizzWithDynamic:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        analytics = AnalyticService(database=db)
        return await analytics.get_users_quizz_dynamic(company_id=company_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Dynamic of rating in company can see only admin or owner')


@router.get('/{company_id}/general/dynamic/{user_id}', status_code=200, response_model=ListQuizzesWithDynamic)
async def get_general_rating_one_member(company_id: int, user_id: int, db: Database = Depends(get_db),
                                        user: User = Depends(get_current_user)) -> ListQuizzesWithDynamic:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    actions = ActionsService(database=db)
    if not await actions.check_user_consists_company(company_id=company_id, user_id=user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User is not member of company')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        analytics = AnalyticService(database=db)
        return await analytics.get_member_quizz_dynamic(company_id=company_id, user_id=user_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Dynamic of user rating in company can see only admin or owner')


@router.get('/{company_id}/last-complete', status_code=200, response_model=ListUserComplete)
async def get_last_complete_in_company(company_id: int, db: Database = Depends(get_db),
                                       user: User = Depends(get_current_user)) -> ListUserComplete:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        analytics = AnalyticService(database=db)
        return await analytics.get_last_complete(company_id=company_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Dynamic of user rating in company can see only admin or owner')
