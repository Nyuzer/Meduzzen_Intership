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


# userfortests@gmail.com
# Password01923
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJmb3J0ZXN0c0BnbWFpbC5jb20iLCJleHBpcnkiOjE2Nzg2NjM2MTQuNDY0NzEwNX0.nVMehaQz-A2FdRLtUS5Gy5Yxq58RJnZPiTb6zPq1Jd0

# 111111user@example.com
# string012345
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjExMTExMXVzZXJAZXhhbXBsZS5jb20iLCJleHBpcnkiOjE2Nzg2NjQ1MTYuNDAxOTI1OH0.T1JNLBGzDmNM0WYegJZ6hh536Ee9nS1mOtyqq7L2sog
@router.post('/login', response_model=TokenResponse)
async def login_for_token(user: SigninUser, db: Database = Depends(get_db)) -> TokenResponse:
    user_service = UserService(database=db)
    if await user_service.user_authentication(user=user):
        return create_access_token(user.email)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
