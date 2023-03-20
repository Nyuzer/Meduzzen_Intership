from fastapi import APIRouter, Depends, status, HTTPException
from databases import Database


from project.schemas.schemas import User, TokenResponse, SigninUser
from project.services.services import get_current_user, UserService
from project.core.security import create_access_token
from project.db.connections import get_db


router = APIRouter()


@router.post('/me', response_model=User)
async def auth_me(user: User = Depends(get_current_user)) -> User:
    return user


# 111111user@example.com
# string012345
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjExMTExMXVzZXJAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE2NzkzMzY1ODEuNTE0NjkzfQ.e2d2tKRlE11PAPAvIZPUDJUmi0bEMM9sgSvslJMftvM

# "id": 32,
# "username": "strasaing",
# "email": "111111user@example.com",

# 010101user@example.com
# Miniasas01234
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjAxMDEwMXVzZXJAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE2NzkzNDkwODUuMDAyOTE5N30.yBvblwojE3W1Eycrev2YIH_ZnBe5qtBJ0iDbA2fecyo

# "id": 8,
# "name": "Miniasas01234",
# "description": "Abiaib",
# "owner_id": 34,

@router.post('/login', response_model=TokenResponse)
async def login_for_token(user: SigninUser, db: Database = Depends(get_db)) -> TokenResponse:
    user_service = UserService(database=db)
    if await user_service.user_authentication(user=user):
        return create_access_token(user.email)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
