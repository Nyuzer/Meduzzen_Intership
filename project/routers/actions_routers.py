from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.schemas.schemas_actions import ListOwnerSendInvite, ListOwnerRequests, ListUserRequests, ListUserInvites,\
    OwnerSendInvite, OwnerSendInvitePost
from project.schemas.schemas import User
from project.db.connections import get_db
from project.services.services import get_current_user, UserService
from project.services.services_company import CompanyService
from project.services.services_actions import ActionsService


router = APIRouter()


# Returns all requests to join the company for owner
@router.get('/company/{pk}', status_code=200, response_model=ListOwnerRequests)
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
@router.get('/company/{pk}/my', status_code=200, response_model=ListOwnerSendInvite)
async def get_company_invites(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ListOwnerSendInvite:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    actions = ActionsService(database=db)
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.get_company_invites(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Invite user to our company
# change response to dict -- {'detail': 'success'}
@router.post('/company/{pk}', status_code=200, response_model=dict)
async def create_invite(pk: int,  invite: OwnerSendInvitePost, db: Database = Depends(get_db),
                        user: User = Depends(get_current_user)) -> dict:
    # remove field from OwnerSendInvite schema
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company does not exist")
    check_user = UserService(database=db)
    if await check_user.get_user(pk=invite.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This user not found')
    actions = ActionsService(database=db)
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.invite_create(invite=invite)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Delete invite to the company
@router.delete('/{pk}', status_code=200)
async def delete_invite(pk: int, db: Database = Depends(get_db), user: User = Depends(get_current_user)):
    actions = ActionsService(database=db)
    company_id = await actions.check_invite_exist(invite_pk=pk)
    if not company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    if await actions.check_owner(company_id=company_id, user_id=user.id):
        return await actions.invite_delete(invite_id=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Returns all requests to join the company for user
@router.get('/my', status_code=200, response_model=ListUserRequests)
async def get_user_req(db: Database = Depends(get_db), user: User = Depends(get_current_user)) -> ListUserRequests:
    actions = ActionsService(database=db)
    return await actions.get_user_requests(user=user)


# Returns all invites to join the company for user
@router.get('/my/invites', status_code=200, response_model=ListUserInvites)
async def get_user_invites(db: Database = Depends(get_db), user: User = Depends(get_current_user)) -> ListUserInvites:
    actions = ActionsService(database=db)
    return await actions.get_user_invites(user=user)
