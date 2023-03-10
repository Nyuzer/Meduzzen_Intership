from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
import sys

sys.path = ['', '..'] + sys.path[1:]

from project.schemas.schemas import User, SigninUser, SignupUser, ListUser, UpdateUser, TokenResponse
from project.services.services import UserService, get_current_user
from project.db.connections import get_db
from project.core.security import create_access_token
from databases import Database

# user_service = UserService(db)

router = APIRouter()


@router.get('/', response_model=ListUser)
async def users_list(page: int = 1, db: Database = Depends(get_db)) -> ListUser:
    user_service = UserService(database=db)
    return await user_service.get_users_list(page=page)


@router.get('/{pk}', response_model=User)
async def user_single(pk: int, db: Database = Depends(get_db)) -> User:
    user_service = UserService(database=db)
    user = await user_service.get_user(pk=pk)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.post('/', status_code=200, response_model=User)
async def user_create(user: SignupUser, db: Database = Depends(get_db)) -> User:
    user_service = UserService(database=db)
    if await UserService.email_exists(db=db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This email is already registered')
    else:
        user = await user_service.creation_user(user=user)
        if user:
            return user
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')


@router.put('/{pk}', status_code=200, response_model=User)
async def user_update(pk: int, user: UpdateUser, db: Database = Depends(get_db)) -> User:
    user_service = UserService(database=db)
    is_user_exist = await user_service.get_user(pk=pk)
    if is_user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if user.hash_password is not None:
        if not UserService.is_acceptable_password(password=user.hash_password):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='The password is unacceptable')
        else:
            user.hash_password = UserService.hash_password(password=user.hash_password)
    return await user_service.update_user(pk=pk, user=user)


@router.delete('/{pk}', status_code=200)
async def user_delete(pk: int, db: Database = Depends(get_db)):
    user_service = UserService(database=db)
    is_user_exist = await user_service.get_user(pk=pk)
    if is_user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    await user_service.delete_user(pk=pk)


# assasasas@example.com
# String123123123lascxz
@router.post('/login', response_model=TokenResponse)
async def login_for_token(user: SigninUser, db: Database = Depends(get_db)) -> TokenResponse:
    user_service = UserService(database=db)
    if await user_service.user_authentication(user=user):
        return create_access_token({'email': user.email})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
