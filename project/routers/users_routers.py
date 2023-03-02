from fastapi import APIRouter, HTTPException, status, Depends
import sys

sys.path = ['', '..'] + sys.path[1:]

from project.schemas.schemas import User, SigninUser, SignupUser, ListUser, UpdateUser
from project.services.services import UserService
from project.db.connections import get_db
from databases import Database

# user_service = UserService(db)

router = APIRouter()


@router.get('/', response_model=ListUser)
async def users_list(db: Database = Depends(get_db)) -> ListUser:
    user_service = UserService(db)
    return await user_service.get_users_list()


@router.get('/{pk}', response_model=User)
async def user_single(pk: int, db: Database = Depends(get_db)) -> User:
    user_service = UserService(db)
    user = await user_service.get_user(pk)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.post('/', status_code=201, response_model=SignupUser)
async def user_create(user: SignupUser, db: Database = Depends(get_db)) -> SignupUser:
    user_service = UserService(db)
    user = await user_service.creation_user(user)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')


# bad working func
@router.put('/{pk}', status_code=201, response_model=UpdateUser)
async def user_update(pk: int, user: UpdateUser, db: Database = Depends(get_db)) -> UpdateUser:
    user_service = UserService(db)
    is_user_exist = await user_service.get_user(pk)
    if is_user_exist is None:
        # Does not return this and give us 500 error
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    return await user_service.update_user(pk, user)


# bad working func
@router.delete('/{pk}', status_code=204)
async def user_delete(pk: int, db: Database = Depends(get_db)):
    user_service = UserService(db)
    is_user_exist = await user_service.get_user(pk)
    if is_user_exist is None:
        # Does not return this
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    return await user_service.delete_user(pk)
