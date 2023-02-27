import os
from dotenv import load_dotenv
import databases
import aioredis

# Make sense to refactor it and put in core package

load_dotenv('.env')

DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

db = databases.Database(DATABASE_URL)


def get_db():
    return db

# REDIS


async def get_redis():
    return aioredis.from_url(os.getenv("REDIS_URL"))
