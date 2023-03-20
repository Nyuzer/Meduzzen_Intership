from project.schemas.schemas_actions import Member, ListMember, ListOwnerRequests, \
    OwnerRequests, ListOwnerSendInvite, OwnerSendInvite, ListUserRequests, UserRequests, ListUserInvites, UserInvites, \
    OwnerSendInvitePost, ResponseSuccess, UserSendAccessionRequest
from project.schemas.schemas_comp import Company
from project.schemas.schemas import User
from project.db.models import company_members, users, actions
from typing import Optional

from project.db.models import companies

from databases import Database


class ActionsService:
    def __init__(self, database: Database):
        self.db = database

    async def retrieve_userid(self, pk: int) -> int:
        query = actions.select().where(actions.c.id == pk)
        item = await self.db.fetch_one(query)
        return item.user_id

    async def check_invite_request_exist(self, pk: int, type_r: str) -> Optional[int]:
        query = actions.select().where(actions.c.id == pk, actions.c.type_of_request == type_r)
        company = await self.db.fetch_one(query)
        if company is not None:
            return company.company_id
        return None

    async def check_request_exist(self, pk: int) -> bool:
        query = actions.select().where(actions.c.id == pk, actions.c.type_of_request == 'accession-request')
        request = await self.db.fetch_one(query)
        return request is not None

    async def check_owner_of_request_invite(self, pk: int, user_id: int) -> bool:
        query = actions.select().where(actions.c.id == pk)
        result = await self.db.fetch_one(query)
        return result.user_id == user_id

    # Fix it
    # same method in services company -> check_access
    async def check_owner(self, company_id: int, user_id: int) -> bool:
        query = companies.select().where(companies.c.id == company_id)
        item = await self.db.fetch_one(query)
        return Company(**item).owner_id == user_id

    async def check_user_consists_company(self, company_id: int, user_id: int) -> bool:
        query = company_members.select().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == user_id)
        item = await self.db.fetch_one(query)
        return item is not None

    async def check_already_sent(self, company_id: int, user_id: int, type_r: str) -> bool:
        query = actions.select().where(actions.c.company_id == company_id, actions.c.user_id == user_id,
                                       actions.c.type_of_request == type_r)
        item = await self.db.fetch_one(query)
        return item is not None

    async def get_company_members(self, pk: int) -> ListMember:
        query = company_members.select().where(company_members.c.company_id == pk)
        members = await self.db.fetch_all(query=query)
        return ListMember(members=[Member(id=item.id, user_id=item.user_id, role=item.role) for item in members])

    async def get_company_requests(self, pk: int) -> ListOwnerRequests:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'accession-request')
        requests = await self.db.fetch_all(query)
        return ListOwnerRequests(result=[OwnerRequests(id=item.id, user_id=item.user_id,
                                                       company_id=item.company_id, type_of_request=item.type_of_request)
                                         for item in requests])

    async def get_company_invites(self, pk: int) -> ListOwnerSendInvite:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'invited')
        invites = await self.db.fetch_all(query)
        return ListOwnerSendInvite(result=[OwnerSendInvite(id=item.id, user_id=item.user_id, company_id=item.company_id,
                                                           invite_message=item.invite_message) for item in invites])

    async def get_user_requests(self, user: User) -> ListUserRequests:
        query = actions.select().where(actions.c.user_id == user.id, actions.c.type_of_request == 'accession-request')
        requests = await self.db.fetch_all(query)
        return ListUserRequests(result=[UserRequests(id=item.id, company_id=item.company_id,
                                                     invite_message=item.invite_message) for item in requests])

    async def get_user_invites(self, user: User) -> ListUserInvites:
        query = actions.select().where(actions.c.user_id == user.id, actions.c.type_of_request == 'invited')
        invites = await self.db.fetch_all(query)
        return ListUserInvites(result=[UserInvites(id=item.id, company_id=item.company_id,
                                                   invite_message=item.invite_message) for item in invites])

    async def invite_create(self, invite: OwnerSendInvitePost, company_id: int) -> ResponseSuccess:
        query = actions.insert().values(company_id=company_id, user_id=invite.user_id, type_of_request='invited',
                                        invite_message=invite.invite_message)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def invite_request_delete(self, pk: int) -> ResponseSuccess:
        query = actions.delete().where(actions.c.id == pk)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def send_user_request(self, request: UserSendAccessionRequest, user_id: int) -> ResponseSuccess:
        query = actions.insert().values(company_id=request.company_id, user_id=user_id,
                                        type_of_request='accession-request', invite_message=request.invite_message)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def accept_user_invite(self, pk: int, company_id: int, user_id: int) -> ResponseSuccess:
        query = actions.delete().where(actions.c.id == pk)
        await self.db.execute(query)
        query = company_members.insert().values(company_id=company_id, user_id=user_id, role='general-user')
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def owner_exclude_user(self, company_id: int, pk: int) -> ResponseSuccess:
        query = company_members.delete().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == pk)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

    async def leaves_user_company(self, company_id: int, user_id: int) -> ResponseSuccess:
        query = company_members.delete().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == user_id)
        await self.db.execute(query)
        return ResponseSuccess(detail='success')

