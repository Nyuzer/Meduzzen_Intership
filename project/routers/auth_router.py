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


@router.post('/login', response_model=TokenResponse)
async def login_for_token(user: SigninUser, db: Database = Depends(get_db)) -> TokenResponse:
    user_service = UserService(database=db)
    if await user_service.user_authentication(user=user):
        return create_access_token(user.email)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


# user@gmail.com
# String123123
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJAZ21haWwuY29tIiwiZXhwaXJ5IjoxNjc5OTUyNTQzLjA3MjE2NTd9.8U_R635TlWKcWTWyGEYcgFVlU7Yx9O25e8MPqwGucmY

# company_id 1

"""
{
  "name": "string",
  "description": "string",
  "number_of_frequency": 0,
  "quiz_questions": [
    {
      "question": "2+2=?",
      "answers": [
        "1",
        "2",
        "3",
        "4"
      ],
      "correct_answer": "4"
    },
    {
      "question": "2+2=?",
      "answers": [
        "1",
        "2",
        "3",
        "4"
      ],
      "correct_answer": "4"
    },
    {
      "question": "2+2=?",
      "answers": [
        "1",
        "2",
        "3",
        "4"
      ],
      "correct_answer": "4"
    }
  ]
}
"""