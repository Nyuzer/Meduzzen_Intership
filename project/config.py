from dotenv import load_dotenv
import os

load_dotenv('.env')

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# {os.getenv("HOST")}
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
