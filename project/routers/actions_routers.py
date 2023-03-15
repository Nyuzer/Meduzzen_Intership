from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.schemas.schemas_actions import ListOwnerSendInvite, ListOwnerRequests
from project.schemas.schemas import User
from project.db.connections import get_db
from project.services.services import get_current_user
from project.services.services_company import CompanyService
from project.services.services_actions import ActionsService


router = APIRouter()


# Returns all requests to join the company
@router.get('/company/{pk}', response_model=ListOwnerRequests)
async def get_company_access_requests(pk: int, db: Database = Depends(get_db),
                                      user: User = Depends(get_current_user)) -> ListOwnerRequests:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    actions = ActionsService(database=db)
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.get_company_requests(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Returns all invites from company to users
@router.get('/company/{pk}/my', response_model=ListOwnerSendInvite)
async def get_company_invites(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ListOwnerSendInvite:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    actions = ActionsService(database=db)
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.get_company_invites(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")
