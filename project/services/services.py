from databases import Database

from project.db.models import users
from project.schemas.schemas import SignupUser, User, ListUser, UpdateUser
from datetime import datetime

import os
import hashlib
from typing import Optional


class UserService:
    def __init__(self, database: Database):
        self.db = database

    # Hashing password
    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        # result[:32] -- salt | result[32:] -- key
        return (salt + key).decode('latin1')

    # Compare entered password with password in storage
    @staticmethod
    def check_hashes(checked_password: str, key_pass: str) -> bool:
        # key_pass -- users hashed password
        key_pass = key_pass.encode('latin1')
        salt, key = key_pass[:32], key_pass[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', checked_password.encode('utf-8'), salt, 100000)
        return new_key == key

    # Check password
    # rewrite
    @staticmethod
    def is_acceptable_password(password: str) -> bool:
        return len(set(password)) > 5 and len(password) >= 8

    # services
    # read all
    async def get_users_list(self) -> ListUser:
        """Return users list"""
        users_list = await self.db.fetch_all(query=users.select())
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
    async def creation_user(self, user: SignupUser) -> SignupUser:
        """Create user. First check password after it create."""
        res_val = UserService.is_acceptable_password(user.hash_password)
        if res_val:
            hashed_password = UserService.hash_password(user.hash_password)
            new_user = users.insert().values(email=user.email, hash_password=hashed_password,
                                             time_created=datetime.utcnow(), time_updated=datetime.utcnow(),
                                             is_root=False)
            created = await self.db.execute(new_user)
            return SignupUser(email=user.email, hash_password=hashed_password, time_created=datetime.utcnow(),
                              time_updated=datetime.utcnow(), is_root=False)
        return res_val

    # update
    # Add hash_password check
    async def update_user(self, pk: int, user: UpdateUser) -> UpdateUser:
        """Update user here.
        Also should rewrite this method, because user can enter any password and add validation for email"""
        info = {k: v for k, v in user.dict().items() if v is not None}
        update_user = users.update().where(users.c.id == pk).values(**info)
        updated = await self.db.execute(update_user)
        return UpdateUser(**info)

    # delete
    async def delete_user(self, pk: int):
        """Delete user"""
        deleted_user = users.delete().where(users.c.id == pk)
        return await self.db.execute(deleted_user)
