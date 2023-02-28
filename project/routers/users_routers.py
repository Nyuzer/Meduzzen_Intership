from typing import List
from fastapi import APIRouter, HTTPException
import sys

sys.path = ['', '..'] + sys.path[1:]

from project.db.models import User
from project.schemas.schemas import User, SigninUser, SignupUser, ListUser, UpdateUser
from project.services import services

router = APIRouter()


@router.get('/', response_model=ListUser)
async def users_list():
    return await services.get_users_list()


@router.get('/{pk}', response_model=User)
async def user_single(pk: int):
    user = await services.get_user(pk)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', status_code=201, response_model=SignupUser)
async def user_create(item: SignupUser):
    return await services.creation_user(item)
