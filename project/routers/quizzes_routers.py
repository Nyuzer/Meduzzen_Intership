from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.services.services import get_current_user

from project.db.connections import get_db

from project.schemas.schemas_quizzes import ListQuizz, Quizz, CreateQuizz, UpdateQuizz, UpdateQuestion, QuizzComplete,\
    QuizzResultComplete
from project.schemas.schemas import User
from project.schemas.schemas_actions import ResponseSuccess

from project.services.services_company import CompanyService
from project.services.services_actions import ActionsService
from project.services.services_quizzes import QuizzService

router = APIRouter()


# Get all quizzes for company
@router.get('/{company_id}', status_code=200, response_model=ListQuizz)
async def get_all_quizzes(company_id: int, db: Database = Depends(get_db),
                          user: User = Depends(get_current_user)) -> ListQuizz:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    actions = ActionsService(database=db)
    if not await actions.check_user_consists_company(company_id=company_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User is not member of company')
    quizzes = QuizzService(database=db)
    return await quizzes.get_quizzes(company_id=company_id)


# Get quizz by id by owner or admin
@router.get('/{company_id}/quizz/{quizz_id}', status_code=200, response_model=Quizz)
async def get_quizz_by_id(company_id: int, quizz_id: int, db: Database = Depends(get_db),
                          user: User = Depends(get_current_user)) -> Quizz:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if not await quizzes.your_company_quizz(quizz_id=quizz_id, company_id=company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not your company quizz')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_get_by_id(quizz_id=quizz_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can read only owner or admin')


# Create quizz by owner or admin
@router.post('/{company_id}/create', status_code=200, response_model=ResponseSuccess)
async def create_quizz(company_id: int, quizz: CreateQuizz, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if await quizzes.check_exist_quizz_by_name(quizz_name=quizz.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz with this name already exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_create(quizz=quizz, company_id=company_id, author_id=user.id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can create only owner or admin')


# Update quizz by owner or admin
@router.put('/{company_id}/update/{quizz_id}', status_code=200, response_model=ResponseSuccess)
async def update_quizz(company_id: int, quizz_id: int, quizz: UpdateQuizz, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if quizz.name is not None:
        if await quizzes.check_exist_quizz_by_name(quizz_name=quizz.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz with this name already exist')
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if not await quizzes.your_company_quizz(quizz_id=quizz_id, company_id=company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Quiz does not belong to your company')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_update(quizz_id=quizz_id, quizz=quizz, updated_by=user.id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can update only owner or admin')


# update quiz questions
@router.put('/{company_id}/update/{quizz_id}/questions/{question_id}', status_code=200, response_model=ResponseSuccess)
async def update_quizz_questions(company_id: int, quizz_id: int, question_id: int, question: UpdateQuestion,
                                 db: Database = Depends(get_db),
                                 user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    actions = ActionsService(database=db)
    if not await actions.check_user_consists_company(company_id=company_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User is not member of company')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if not await quizzes.check_exists_question(question_id=question_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question does not exist')
    if not await quizzes.your_company_quizz(quizz_id=quizz_id, company_id=company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Quiz does not belong to your company')
    if not await quizzes.question_related_to_quizz(quizz_id=quizz_id, question_id=question_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Question does not related to your quizz')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.validate_question(database=db, question=question, question_id=question_id, user_id=user.id,
                                               quizz_id=quizz_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Question can update only owner or admin')


# Delete quizz by owner or admin
@router.delete('/{company_id}/delete/{quizz_id}', status_code=200, response_model=ResponseSuccess)
async def delete_quizz(company_id: int, quizz_id: int, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if not await quizzes.your_company_quizz(quizz_id=quizz_id, company_id=company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not your company quizz')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_delete(quizz_id=quizz_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can create only owner or admin')


# Quizz completion
# только один эндпоинт прохождения
# функционал что оно считает рейтинг и средний балл
@router.post('/{company_id}/completion/{quizz_id}', status_code=200, response_model=QuizzResultComplete)
async def complete_quizz(company_id: int, quizz_id: int, res: QuizzComplete, db: Database = Depends(get_db),
                         user: User = Depends(get_current_user)) -> QuizzResultComplete:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    actions = ActionsService(database=db)
    if not await actions.check_user_consists_company(company_id=company_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User is not member of company')
    if not await quizzes.your_company_quizz(quizz_id=quizz_id, company_id=company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not your company quizz')
    return await quizzes.quizz_complete(quizz_id=quizz_id, company_id=company_id, user_id=user.id, results=res)


@router.get('/aba/my', status_code=200)
async def example_1(db: Database = Depends(get_db),
                    user: User = Depends(get_current_user)):
    quizzes = QuizzService(database=db)
    return await quizzes.get_user_general_rating(user_id=user.id)
