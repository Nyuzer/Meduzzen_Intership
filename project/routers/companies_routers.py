from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.services.services import get_current_user
from project.services.services_company import CompanyService
from project.services.services_actions import ActionsService
from project.schemas.schemas import User
from project.schemas.schemas_comp import Company, CompanyCreate, CompanyUpdate, ListCompany
from project.schemas.schemas_actions import ListMember
from project.db.connections import get_db

router = APIRouter()


@router.get('/', response_model=ListCompany)
async def companies_list(page: int = 1, db: Database = Depends(get_db),
                         authenticated: User = Depends(get_current_user)) -> ListCompany:
    companies = CompanyService(database=db)
    return await companies.get_companies_list(page=page)


@router.get('/{pk}', response_model=Company)
async def company_single(pk: int, db: Database = Depends(get_db),
                         authenticated: User = Depends(get_current_user)) -> Company:
    companies = CompanyService(database=db)
    company = await companies.get_company(pk=pk)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    return company


@router.post('/', status_code=201, response_model=Company)
async def company_create(company: CompanyCreate, db: Database = Depends(get_db),
                         user: User = Depends(get_current_user)) -> Company:
    companies = CompanyService(database=db)
    if await companies.company_exists(name=company.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This name is already exist')
    company_new = await companies.company_create(user_id=user.id, company=company)
    if company_new:
        return company_new
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid information')


@router.put('/{pk}', status_code=200, response_model=Company)
async def company_update(pk: int, company: CompanyUpdate, db: Database = Depends(get_db),
                         user: User = Depends(get_current_user)) -> Company:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    if await companies.check_access(company_pk=pk, user_id=user.id):
        if await companies.update_company(pk=pk, company=company):
            return await companies.get_company(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")


@router.delete('/{pk}', status_code=200)
async def company_delete(pk: int, db: Database = Depends(get_db), user: User = Depends(get_current_user)):
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    if await companies.check_access(company_pk=pk, user_id=user.id):
        return await companies.delete_company(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")


# userexample@example.com
# UserExample321
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJleGFtcGxlQGV4YW1wbGUuY29tIiwiZXhwaXJ5IjoxNjc4OTE5MTk2LjYwNTYyMDR9.qoZz3haGjcfncbIYxMO2yKPR24W14gzCYLV-44ICPgk
# comp id = 6
@router.get('/{pk}/members', status_code=200, response_model=ListMember)
async def company_get_members(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ListMember:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    actions = ActionsService(database=db)
    return await actions.get_company_members(pk=pk)

