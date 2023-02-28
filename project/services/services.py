from project.db.connections import db
from project.db.models import users
from project.schemas.schemas import SignupUser

import os
import hashlib


# Make a class better solution

async def get_users_list():
    users_list = await db.fetch_all(query=users.select())
    return [dict(user) for user in users_list]


async def get_user(pk: int):
    query = f'SELECT id, username, email, is_root, status, time_created, time_updated FROM users WHERE id={pk}'
    user = await db.fetch_one(query=query)
    if user is not None:
        user = dict(user)
        return user
    return None


# add logic how to create user
async def creation_user(item: SignupUser):
    pass


# Hashing password
def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # result[:32] -- salt | result[32:] -- key
    return salt + key


# Compare entered password with password in storage
def check_hashes(checked_password: str, key_pass: str) -> bool:
    # key_pass -- users hashed password
    salt, key = key_pass[:32], key_pass[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', checked_password.encode('utf-8'), salt, 100000)
    return new_key == key


# Check password
def is_acceptable_password(password: str) -> bool:
    collect = set(password)
    if len(list(filter(lambda x: x.isdigit(), collect))) >= 3 or \
            len(list(filter(lambda x: x.isalpha(), collect))) >= 3 or(\
            len(list(filter(lambda x: x.isdigit(), collect))) +\
            len(list(filter(lambda x: x.isalpha(), collect))) >= 3):
        if len(password) >= 9 and 'password' not in password.lower():
            return True
        elif 'password' not in password.lower():
            return len(password) > 6 and 0 < len(list(filter(lambda x: x.isdigit(), password))) < len(password)
    return False


