from fastapi import APIRouter, Depends

from project.schemas.schemas import User
from project.services.services import get_current_user

router = APIRouter()


@router.post('/me', response_model=User)
async def auth_me(user: User = Depends(get_current_user)) -> User:
    return user
