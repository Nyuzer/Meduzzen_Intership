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
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJAZ21haWwuY29tIiwiZXhwaXJ5IjoxNjgwMDc3MDcxLjgwMDk0Njd9.86V1CeTRpjf8fbKA10PMH78Lbq82Bc--cP6y3fo_QOo

# user1@example.com
# String123123
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXIxQGV4YW1wbGUuY29tIiwiZXhwaXJ5IjoxNjgwMDI4NDU5LjYyMjQ0MzR9.nT75efTuMOfVNXMFuqvfXiaCOdQI96ZCO6gB_4ntn6A

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