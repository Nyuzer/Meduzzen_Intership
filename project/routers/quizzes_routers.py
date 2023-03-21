from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.services.services import get_current_user

from project.db.connections import get_db

from project.schemas.schemas_quizzes import ListQuizz, Quizz, CreateQuizz, UpdateQuizz
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
                            detail=f'User with id {user.id} is not member of company')
    quizzes = QuizzService(database=db)
    return await quizzes.get_quizzes(company_id=company_id)


# Create quizz by owner or admin
@router.post('/{company_id}/create', status_code=200, response_model=ResponseSuccess)
async def create_quizz(company_id: int, quizz: CreateQuizz, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        quizzes = QuizzService(database=db)
        return await quizzes.quizz_create(quizz=quizz, company_id=company_id, author_id=user.id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can create only owner or admin')


@router.put('/{company_id}/update/{quizz_id}', status_code=200, response_model=ResponseSuccess)
async def update_quizz(company_id: int, quizz_id: int, quizz: UpdateQuizz, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_update(quizz_id=quizz_id, quizz=quizz)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can create only owner or admin')


@router.delete('/{company_id}/delete/{quizz_id}', status_code=200, response_model=ResponseSuccess)
async def delete_quizz(company_id: int, quizz_id: int, db: Database = Depends(get_db),
                       user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The company does not exist')
    quizzes = QuizzService(database=db)
    if not await quizzes.check_exist_quizz(quizz_id=quizz_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Quizz does not exist')
    if await companies.is_an_admin(company_id=company_id, user_id=user.id) or \
            await companies.check_access(company_pk=company_id, user_id=user.id):
        return await quizzes.quizz_delete(quizz_id=quizz_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quizz can create only owner or admin')
