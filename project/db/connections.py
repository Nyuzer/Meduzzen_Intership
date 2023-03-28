import os
from dotenv import load_dotenv
import databases
import aioredis

# Make sense to refactor it and put in core package

load_dotenv('.env')

DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@' \
               f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

db = databases.Database(DATABASE_URL)

TEST_DATABASE_URL = f'postgresql://{os.getenv("TEST_POSTGRES_USER")}:{os.getenv("TEST_POSTGRES_PASSWORD")}@' \
               f'{os.getenv("TEST_POSTGRES_HOST")}:{os.getenv("TEST_POSTGRES_PORT")}/{os.getenv("TEST_POSTGRES_DB")}'


def get_db():
    return db

# REDIS


async def get_redis():
    return aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
