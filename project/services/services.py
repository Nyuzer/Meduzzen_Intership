from project.db.connections import db
from project.db.models import users
from project.schemas.schemas import SignupUser, User, ListUser, UpdateUser
from datetime import datetime

import os
import hashlib
from typing import Optional


class UserService:
    def __init__(self, database):
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
    @staticmethod
    def is_acceptable_password(password: str) -> bool:
        collect = set(password)
        if len(list(filter(lambda x: x.isdigit(), collect))) >= 3 or \
                len(list(filter(lambda x: x.isalpha(), collect))) >= 3 or (
                        len(list(filter(lambda x: x.isdigit(), collect))) +
                        len(list(filter(lambda x: x.isalpha(), collect))) >= 3):
            if len(password) >= 9 and 'password' not in password.lower():
                return True
            elif 'password' not in password.lower():
                return len(password) > 6 and 0 < len(list(filter(lambda x: x.isdigit(), password))) < len(password)
        return False

    # services
    # read all
    async def get_users_list(self) -> ListUser:
        users_list = await self.db.fetch_all(query=users.select())
        return ListUser(users=[User(**item) for item in users_list])

    # read single
    async def get_user(self, pk: int) -> Optional[User]:
        query = users.select().where(users.c.id == pk)
        user = await self.db.fetch_one(query=query)
        if user is not None:
            return User(**user)
        return None

    # create
    async def creation_user(self, user: SignupUser) -> SignupUser:
        # check password
        res_val = UserService.is_acceptable_password(user.hash_password)
        if res_val:
            hashed_password = UserService.hash_password(user.hash_password)
            new_user = users.insert().values(email=user.email, hash_password=hashed_password,
                                             time_created=datetime.utcnow(), time_updated=datetime.utcnow(),
                                             is_root=False)
            return await db.execute(new_user)
        return res_val

    # update
    # Add hash_password check
    async def update_user(self, pk: int, user: UpdateUser) -> UpdateUser:
        update_user = users.update().where(users.c.id == pk).values(**user.dict())
        return await db.execute(update_user)

    # delete
    async def delete_user(self, pk: int):
        deleted_user = users.delete().where(users.c.id == pk)
        if deleted_user is not None:
            return await db.execute(deleted_user)
        return None
