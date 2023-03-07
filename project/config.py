from dotenv import load_dotenv
import os

load_dotenv('.env')

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# {os.getenv("HOST")}
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGERS_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@' \
               f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

REDIS_URL = os.getenv("REDIS_URL")

TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
TEST_POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT")

TEST_DATABASE_URI = f'postgresql+asyncpg://{os.getenv("TEST_POSTGRES_USER")}:{os.getenv("TEST_POSTGRES_PASSWORD")}@' \
               f'{os.getenv("TEST_POSTGRES_HOST")}:{os.getenv("TEST_POSTGRES_PORT")}/{os.getenv("TEST_POSTGRES_DB")}'

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
