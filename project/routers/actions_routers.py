from fastapi import APIRouter, HTTPException, status, Depends
from databases import Database

from project.schemas.schemas_actions import ListOwnerSendInvite, ListOwnerRequests, ListUserRequests, ListUserInvites,\
    OwnerSendInvitePost, ResponseSuccess, UserRequests, UserSendAccessionRequest
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
    actions = ActionsService(database=db)
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.get_company_invites(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Invite user in the company
@router.post('/company/{pk}', status_code=200, response_model=ResponseSuccess)
async def create_invite(pk: int,  invite: OwnerSendInvitePost, db: Database = Depends(get_db),
                        user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
    check_user = UserService(database=db)
    if await check_user.get_user(pk=invite.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This user not found')
    actions = ActionsService(database=db)
    if await actions.check_already_sent(company_id=pk, user_id=invite.user_id, type_r='invited'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Request already sent')
    if await actions.check_user_consists_company(company_id=pk, user_id=invite.user_id):
        raise HTTPException(status_code=status.status.HTTP_400_BAD_REQUEST,
                            detail="User is already a member of the company")
    if await actions.check_owner(company_id=pk, user_id=user.id):
        return await actions.invite_create(invite=invite, company_id=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Delete invite to the company
@router.delete('/{pk}', status_code=200, response_model=ResponseSuccess)
async def delete_invite(pk: int, db: Database = Depends(get_db),
                        user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    company_id = await actions.check_invite_request_exist(pk=pk, type_r='invited')
    if not company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    if await actions.check_owner(company_id=company_id, user_id=user.id):
        return await actions.invite_request_delete(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Owner accept request
@router.get('/company/{pk}/accept', status_code=200, response_model=ResponseSuccess)
async def owner_accept_request(pk: int, db: Database = Depends(get_db),
                               user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    company_id = await actions.check_invite_request_exist(pk=pk, type_r='accession-request')
    if not company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Request not found')
    if await actions.check_owner(company_id=company_id, user_id=user.id):
        user_id = await actions.retrieve_userid(pk=pk)
        return await actions.accept_user_invite(pk=pk, company_id=company_id, user_id=user_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Owner decline request
@router.get('/company/{pk}/decline', status_code=200, response_model=ResponseSuccess)
async def owner_decline_request(pk: int, db: Database = Depends(get_db),
                                user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    company_id = await actions.check_invite_request_exist(pk=pk, type_r='accession-request')
    if not company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Request not found')
    if await actions.check_owner(company_id=company_id, user_id=user.id):
        return await actions.invite_request_delete(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="it's not your company")


# Owner can exclude user from company
@router.delete('/company/{company_id}/exclude/{pk}', status_code=200, response_model=ResponseSuccess)
async def owner_exclude_user(company_id: int, pk: int, db: Database = Depends(get_db),
                             user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
    actions = ActionsService(database=db)
    if not await actions.check_user_consists_company(company_id=company_id, user_id=pk):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found')
    if await actions.check_owner(company_id=company_id, user_id=user.id):
        return await actions.owner_exclude_user(company_id=company_id, pk=pk)
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


# User quits the company
@router.get('/my/{pk}/quit', status_code=200, response_model=ResponseSuccess)
async def user_leaves_company(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=pk) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
    actions = ActionsService(database=db)
    if await actions.check_user_consists_company(company_id=pk, user_id=user.id):
        return await actions.leaves_user_company(company_id=pk, user_id=user.id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user does not consists in this company")


# User send an accession request to company
@router.post('/send', status_code=200, response_model=ResponseSuccess)
async def user_send_request(request: UserSendAccessionRequest, db: Database = Depends(get_db),
                            user: User = Depends(get_current_user)) -> ResponseSuccess:
    companies = CompanyService(database=db)
    if await companies.get_company(pk=request.company_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
    actions = ActionsService(database=db)
    if await actions.check_already_sent(company_id=request.company_id, user_id=user.id, type_r='accession-request'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Request already sent')
    if await actions.check_user_consists_company(company_id=request.company_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of the company")
    return await actions.send_user_request(request=request, user_id=user.id)


# User cancel his request
@router.delete('/send/cancel/{pk}', status_code=200, response_model=ResponseSuccess)
async def user_cancel_request(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    if not await actions.check_request_exist(pk=pk):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    if await actions.check_owner_of_request_invite(pk=pk, user_id=user.id):
        return await actions.invite_request_delete(pk=pk)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your request")


# User accept invite
@router.get('/{pk}/accept', status_code=200, response_model=ResponseSuccess)
async def user_accept_invite(pk: int, db: Database = Depends(get_db),
                             user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    company_id = await actions.check_invite_request_exist(pk=pk, type_r='invited')
    if not company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invite not found')
    if await actions.check_owner_of_request_invite(pk=pk, user_id=user.id):
        return await actions.accept_user_invite(pk=pk, company_id=company_id, user_id=user.id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your invite")


# User decline invite
@router.get('/{pk}/decline', status_code=200, response_model=ResponseSuccess)
async def user_decline_invite(pk: int, db: Database = Depends(get_db),
                              user: User = Depends(get_current_user)) -> ResponseSuccess:
    actions = ActionsService(database=db)
    if not await actions.check_invite_request_exist(pk=pk, type_r='invited'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invite not found')
    if await actions.check_owner_of_request_invite(pk=pk, user_id=user.id):
        return await actions.invite_request_delete(pk=pk)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your invite")
