from fastapi import APIRouter, HTTPException, status, Depends

from databases import Database

from project.services.services import get_current_user

from project.db.connections import get_db

from project.schemas.schemas_notifications import ListHiddenNotification, Notification
from project.schemas.schemas import User

from project.services.services_notification import NotificationService

router = APIRouter()


@router.get('/my', status_code=200, response_model=ListHiddenNotification)
async def get_all_notifications(db: Database = Depends(get_db),
                                user: User = Depends(get_current_user)) -> ListHiddenNotification:
    notifications = NotificationService(database=db)
    return await notifications.get_notifications(user_id=user.id)


@router.get('/my/read/{notification_id}', status_code=200, response_model=Notification)
async def read_notification(notification_id: int, db: Database = Depends(get_db),
                            user: User = Depends(get_current_user)) -> Notification:
    notifications = NotificationService(database=db)
    if await notifications.check_notification(notification_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Notification does not exist')
    if await notifications.notification_belongs_user(not_id=notification_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This notification is not your')
    return await notifications.get_notification(not_id=notification_id)
