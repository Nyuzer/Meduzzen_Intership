from fastapi import HTTPException, status, Depends
from project.db.connections import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from databases import Database

from project.db.models import users
from project.schemas.schemas import SignupUser, User, ListUser, UpdateUser, SigninUser, TokenResponse
from project.core.security import decode_token, VerifyToken
from datetime import datetime
import bcrypt

from typing import Optional
import random


class UserService:
    def __init__(self, database: Database):
        self.db = database

    # Hashing password
    @staticmethod
    def hash_password(password: str) -> str:
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).decode('utf-8')

    # Compare entered password with password in storage
    @staticmethod
    def check_hashes(checked_password: str, key_pass: str) -> bool:
        # key_pass -- users hashed password
        checked_password = checked_password.encode('utf-8')
        return bcrypt.checkpw(checked_password, key_pass.encode('utf-8'))

    # Check password
    @staticmethod
    def is_acceptable_password(password: str) -> bool:
        return len(set(password)) > 5 and len(password) >= 8

    # To return schema User for update method
    @staticmethod
    async def get_updated_user_for_method_update(db: Database, pk: int) -> User:
        user = await db.fetch_one(users.select().where(users.c.id == pk))
        return User(**user)

    # Check email if exists
    @staticmethod
    async def email_exists(db: Database, email: str) -> bool:
        user_by_email = await db.fetch_one(users.select().where(users.c.email == email))
        if user_by_email is not None:
            return True
        return False

    # fetch user by email
    @staticmethod
    async def user_by_email(db: Database, email: str) -> User:
        user = await db.fetch_one(users.select().where(users.c.email == email))
        return User(**user)

    # generate random username and password
    @staticmethod
    def faker_user(email: str) -> SignupUser:
        username = 'user_' + str(random.randint(1000000, 9999999))
        hash_password = ''.join([random.choice('A B C D E F G H I K L M N O P Q R S T V X Y Z'.split())
                                 for i in range(10)])
        hash_password += ''.join([str(random.choice(list(range(100, 1000)))) for i in range(5)])
        return SignupUser(email=email, username=username, hash_password=hash_password)

    # authenticate user
    async def user_authentication(self, user: SigninUser) -> bool:
        if await UserService.email_exists(db=self.db, email=user.email):
            user_db = await self.db.fetch_one(users.select().where(users.c.email == user.email))
            user_db = UpdateUser(**user_db)
            return UserService.check_hashes(checked_password=user.hash_password,
                                            key_pass=user_db.hash_password)
        return False

    # services
    # read all
    async def get_users_list(self, page) -> ListUser:
        """Return users list with pagination"""
        limit = 10
        query = users.select()
        offset_page = page - 1
        query = (query.offset(offset_page * limit).limit(limit))
        users_list = await self.db.fetch_all(query=query)
        return ListUser(users=[User(**item) for item in users_list])

    # read single
    async def get_user(self, pk: int) -> Optional[User]:
        """Return user by pk"""
        query = users.select().where(users.c.id == pk)
        user = await self.db.fetch_one(query=query)
        if user is not None:
            return User(**user)
        return None

    # create
    async def creation_user(self, user: SignupUser) -> User:
        """Create user. First check password after it create."""
        res_val = UserService.is_acceptable_password(user.hash_password)
        if res_val:
            hashed_password = UserService.hash_password(user.hash_password)
            new_user = users.insert().values(email=user.email, hash_password=hashed_password, username=user.username,
                                             time_created=datetime.utcnow(), time_updated=datetime.utcnow(),
                                             is_root=False)
            created = await self.db.execute(new_user)
            return User(id=created, email=user.email, time_created=datetime.utcnow(),
                        username=user.username, time_updated=datetime.utcnow(), is_root=False)
        return res_val

    # update
    async def update_user(self, pk: int, user: UpdateUser) -> User:
        """Update user here."""
        info = {k: v for k, v in user.dict().items() if v is not None}
        update_user = users.update().where(users.c.id == pk).values(**info)
        updated = await self.db.execute(update_user)
        return await UserService.get_updated_user_for_method_update(db=self.db, pk=pk)

    # delete
    async def delete_user(self, pk: int):
        """Delete user"""
        deleted_user = users.delete().where(users.c.id == pk)
        await self.db.execute(deleted_user)


token_auth_scheme = HTTPBearer()


# func to find id by email and return User
async def get_current_user(token: TokenResponse = Depends(token_auth_scheme), db: Database = Depends(get_db)) -> User:
    email = decode_token(token=token)
    if email:
        return await UserService.user_by_email(db=db, email=email)
    result = VerifyToken(token.credentials).verify()
    if result.get('status'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token incorrect.")
    else:
        if result.get('user_email'):
            if await UserService.email_exists(db=db, email=result.get('user_email')):
                return await UserService.user_by_email(db=db, email=result.get('user_email'))
            user_service = UserService(database=db)
            return await user_service.creation_user(user=UserService.faker_user(email=result.get('user_email')))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token incorrect.")
