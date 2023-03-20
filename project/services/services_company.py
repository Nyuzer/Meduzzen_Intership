from project.schemas.schemas_comp import Company, CompanyCreate, CompanyUpdate, ListCompany
from project.db.models import companies, company_members
from project.schemas.schemas_actions import ResponseSuccess, ListMember, Member

from datetime import datetime

from typing import Optional

from databases import Database


class CompanyService:
    def __init__(self, database: Database):
        self.db = database

    async def is_an_admin(self, company_id: int, user_id: int) -> bool:
        query = company_members.select().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == user_id)
        member = await self.db.fetch_one(query)
        return member.role == 'admin'

    async def check_access(self, company_pk: int, user_id: int) -> bool:
        """Check user access"""
        company = await self.db.fetch_one(companies.select().where(companies.c.id == company_pk,
                                                                   companies.c.owner_id == user_id))
        if company:
            return True
        return False

    async def company_exists(self, name: str) -> bool:
        """Check by name if company exists"""
        company_by_name = await self.db.fetch_one(companies.select().where(companies.c.name == name))
        if company_by_name is not None:
            return True
        return False

    # get list
    async def get_companies_list(self, page) -> ListCompany:
        """Return companies list with pagination"""
        limit = 10
        query = companies.select()
        offset_page = page - 1
        query = (query.offset(offset_page * limit).limit(limit))
        companies_list = await self.db.fetch_all(query=query)
        return ListCompany(companies=[Company(**item) for item in companies_list])

    # get single
    async def get_company(self, pk: int) -> Optional[Company]:
        """Return company by pk"""
        query = companies.select().where(companies.c.id == pk)
        company = await self.db.fetch_one(query=query)
        if company is not None:
            return Company(**company)
        return None

    # create
    async def company_create(self, user_id: int, company: CompanyCreate) -> Company:
        """Create a new company and add owner"""
        if not company.name:
            return None
        query = companies.insert().values(name=company.name, description=company.description, owner_id=user_id,
                                          time_created=datetime.utcnow(), time_updated=datetime.utcnow())
        created = await self.db.execute(query)
        await self.db.execute(company_members.insert().values(user_id=user_id, company_id=created, role=u'owner'))
        return Company(id=created, name=company.name, description=company.description, owner_id=user_id,
                       time_created=datetime.utcnow(), time_updated=datetime.utcnow())

    # update
    async def update_company(self, pk: int, company: CompanyUpdate) -> bool:
        """Update company"""
        info = {k: v for k, v in company.dict().items() if v is not None}
        query = companies.update().where(companies.c.id == pk).values(**info)
        await self.db.execute(query)
        return True

    # delete
    async def delete_company(self, pk: int):
        """Delete company"""
        query = companies.delete().where(companies.c.id == pk)
        await self.db.execute(query)

    # create an admin
    async def admin_create(self, company_id: int, user_id: int) -> ResponseSuccess:
        """Create an admin"""
        query = company_members.update().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == user_id).values(role='admin')
        await self.db.execute(query)
        return ResponseSuccess(detail="success")

    # delete an admin
    async def admin_remove(self, company_id: int, user_id: int) -> ResponseSuccess:
        """Remove an admin"""
        query = company_members.update().where(company_members.c.company_id == company_id,
                                               company_members.c.user_id == user_id).values(role='general-user')
        await self.db.execute(query)
        return ResponseSuccess(detail="success")

    # get all admins
    async def get_admins_all(self, company_id: int) -> ListMember:
        query = company_members.select().where(company_members.c.company_id == company_id,
                                               company_members.c.role == 'admin')
        admins = await self.db.fetch_all(query)
        return ListMember(members=[Member(id=item.id, user_id=item.user_id, role=item.role) for item in admins])
