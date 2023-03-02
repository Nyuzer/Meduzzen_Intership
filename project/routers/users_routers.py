from typing import List
from fastapi import APIRouter, HTTPException
import sys

sys.path = ['', '..'] + sys.path[1:]

from project.db.models import User
from project.schemas.schemas import User, SigninUser, SignupUser, ListUser, UpdateUser
from project.services.services import UserService
from project.db.connections import db

user_service = UserService(db)

router = APIRouter()


@router.get('/', response_model=ListUser)
async def users_list():
    return await user_service.get_users_list()


@router.get('/{pk}', response_model=User)
async def user_single(pk: int):
    user = await user_service.get_user(pk)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', status_code=201, response_model=SignupUser)
async def user_create(user: SignupUser):
    acception = await user_service.creation_user(user)
    if acception:
        return {'Detail': 'Success'}
    raise HTTPException(status_code=400, detail='Invalid password')


@router.put('/{pk}', status_code=201, response_model=UpdateUser)
async def user_update(pk: int, user: UpdateUser):
    updated = await user_service.update_user(pk, user)
    print(updated, '#####################################')
    # if updated is None make error
    """
    meduzzenintership-web-1    | pydantic.error_wrappers.ValidationError: 1 validation error for UpdateUser
    meduzzenintership-web-1    | response
    meduzzenintership-web-1    |   value is not a valid dict (type=type_error.dict)
    """
    if updated is None:
        return HTTPException(status_code=404, detail="the user does not exist. Can't update.")
    return {'Detail': 'Success'}


@router.delete('/{pk}', status_code=204)
async def user_delete(pk: int):
    delete = await user_service.delete_user(pk)
    print(delete, '#######################################')
    """
    INFO:     172.20.0.1:62938 - "DELETE /users/34 HTTP/1.1" 204 No Content
    """
    if delete is None:
        return HTTPException(status_code=404, detail="The user does not exist. Can't delete.")
    return delete
