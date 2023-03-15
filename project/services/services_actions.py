from project.schemas.schemas_actions import Member, ListMember, ListOwnerRequests, \
    OwnerRequests, ListOwnerSendInvite, OwnerSendInvite
from project.schemas.schemas_comp import Company
from project.db.models import company_members, users, actions

from project.db.models import companies

from databases import Database


class ActionsService:
    def __init__(self, database: Database):
        self.db = database

    async def get_company_members(self, pk: int) -> ListMember:
        query = company_members.select().where(company_members.c.company_id == pk)
        # add query where select username and change schema Member
        # query = company_members.select().where(company_members.c.company_id == pk)
        members = await self.db.fetch_all(query=query)
        return ListMember(members=[Member(id=item.id, user_id=item.user_id, role=item.role) for item in members])

    async def check_owner(self, company_id: int, user_id: int) -> bool:
        query = companies.select().where(companies.c.id == company_id)
        item = await self.db.fetch_one(query)
        return Company(**item).owner_id == user_id

    async def get_company_requests(self, pk: int) -> ListOwnerRequests:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'accession-request')
        requests = await self.db.fetch_all(query)
        return ListOwnerRequests(result=[OwnerRequests(
            id=item.id, user_id=item.user_id, company_id=item.company_id, type_of_request=item.type_of_request) for item in requests])

    async def get_company_invites(self, pk: int) -> ListOwnerSendInvite:
        query = actions.select().where(actions.c.company_id == pk, actions.c.type_of_request == 'invited')
        invites = await self.db.fetch_all(query)
        return ListOwnerSendInvite(result=[OwnerSendInvite(
            id=item.id, user_id=item.user_id, company_id=item.company_id, invite_message=item.invite_message)
            for item in invites])
