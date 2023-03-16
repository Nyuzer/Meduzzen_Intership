from project.schemas.schemas_actions import Member, ListMember, ListOwnerRequests, \
    OwnerRequests, ListOwnerSendInvite, OwnerSendInvite, ListUserRequests, UserRequests, ListUserInvites, UserInvites, \
    OwnerSendInvitePost
from project.schemas.schemas_comp import Company
from project.schemas.schemas import User
from project.db.models import company_members, users, actions

from project.db.models import companies

from databases import Database


class ActionsService:
    def __init__(self, database: Database):
        self.db = database

    async def check_invite_exist(self, invite_pk: int) -> int:
        query = actions.select().where(actions.c.id == invite_pk, actions.c.type_of_request == 'invited')
        company = await self.db.fetch_one(query)
        if company is not None:
            return company.company_id
        return None

    async def check_owner(self, company_id: int, user_id: int) -> bool:
        query = companies.select().where(companies.c.id == company_id)
        item = await self.db.fetch_one(query)
        return Company(**item).owner_id == user_id

    async def get_company_members(self, pk: int) -> ListMember:
        query = company_members.select().where(company_members.c.company_id == pk)
        # add query where select username and change schema Member
        # query = company_members.select().where(company_members.c.company_id == pk)
        members = await self.db.fetch_all(query=query)
        return ListMember(members=[Member(id=item.id, user_id=item.user_id, role=item.role) for item in members])

    async def get_company_requests(self, pk: int) -> ListOwnerRequests:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'accession-request')
        requests = await self.db.fetch_all(query)
        return ListOwnerRequests(result=[OwnerRequests(
            user_id=item.user_id, company_id=item.company_id, type_of_request=item.type_of_request)
            for item in requests])

    async def get_company_invites(self, pk: int) -> ListOwnerSendInvite:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'invited')
        invites = await self.db.fetch_all(query)
        return ListOwnerSendInvite(result=[OwnerSendInvite(id=item.id, user_id=item.user_id, company_id=item.company_id,
                                                           invite_message=item.invite_message) for item in invites])

    async def get_user_requests(self, user: User) -> ListUserRequests:
        query = actions.select().where(actions.c.user_id == user.id, actions.c.type_of_request == 'accession-request')
        requests = await self.db.fetch_all(query)
        return ListUserRequests(result=[UserRequests(company_id=item.id) for item in requests])

    async def get_user_invites(self, user: User) -> ListUserInvites:
        query = actions.select().where(actions.c.user_id == user.id, actions.c.type_of_request == 'invited')
        invites = await self.db.fetch_all(query)
        return ListUserInvites(result=[UserInvites(
            company_id=item.company_id, invite_message=item.invite_message) for item in invites])

    async def invite_create(self, invite: OwnerSendInvitePost) -> dict:
        query = actions.insert().values(company_id=invite.company_id, user_id=invite.user_id, type_of_request='invited',
                                        invite_message=invite.invite_message)
        await self.db.execute(query)
        return {'detail': 'success'}

    async def invite_delete(self, invite_id: int) -> dict:
        query = actions.delete().where(actions.c.id == invite_id)
        await self.db.execute(query)
        return {'detail': 'success'}
