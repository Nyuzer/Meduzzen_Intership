from databases import Database

from sqlalchemy import select

from datetime import datetime

from project.db.models import notifications

from project.schemas.schemas_actions import ListMember
from project.schemas.schemas_notifications import ListHiddenNotification, HiddenNotification, Notification


class NotificationService:
    def __init__(self, database: Database):
        self.db = database

    async def check_notification(self, not_id: int) -> bool:
        query = select(notifications.c.id).where(notifications.c.id == not_id).select_from(notifications)
        res = await self.db.fetch_one(query)
        if res is None:
            return True
        return False

    async def notification_belongs_user(self, not_id: int, user_id: int) -> bool:
        query = select(notifications.c.id).where(notifications.c.id == not_id, notifications.c.user_id == user_id)\
            .select_from(notifications)
        res = await self.db.fetch_one(query)
        if res is None:
            return True
        return False

    async def create_notification(self, company_id: int, quizz_id: int, users_id: ListMember):
        result = []
        time_created = datetime.utcnow()
        for item in users_id.members:
            result.append({'user_id': item.user_id, 'time_created': time_created, 'status': 'sent',
                           'message': f'Company {company_id} created quiz {quizz_id}.'
                                      f' Follow this link - 127.0.0.1:8000/quizz/{company_id}/completion/{quizz_id}'})
        query = notifications.insert().values(result)
        await self.db.execute(query)

    async def get_notifications(self, user_id: int) -> ListHiddenNotification:
        query = select(notifications.c.id, notifications.c.status, notifications.c.time_created).where(notifications.c.user_id == user_id)\
            .select_from(notifications).order_by(notifications.c.time_created.desc())
        result = await self.db.fetch_all(query)
        return ListHiddenNotification(result=[HiddenNotification(id=item.id, status=item.status,
                                                                 received=item.time_created)
                                              for item in result])

    async def get_notification(self, not_id: int) -> Notification:
        query = select(notifications.c.id, notifications.c.time_created, notifications.c.status, notifications.c.message)\
            .where(notifications.c.id == not_id).select_from(notifications)
        result = await self.db.fetch_one(query)
        if result.status == 'sent':
            query = notifications.update().where(notifications.c.id == not_id).values(status='read')
            await self.db.execute(query)
        return Notification(id=result.id, received=result.time_created, status=result.status, message=result.message)
