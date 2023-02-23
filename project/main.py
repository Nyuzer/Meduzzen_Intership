import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import databases
import aioredis

# add environment variables
load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URI')

database = databases.Database(DATABASE_URL)

app = FastAPI()

# add CORS
origins = [
    "http://0.0.0.0:8000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Error
# socket.gaierror: [Errno 8] nodename nor servname provided, or not known
@app.on_event("startup")
async def startup():
    await database.connect()


# Error
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Error
@app.on_event("startup")
async def startup_redis():
    redis = await aioredis.from_url('redis://redis')


@app.get('/')
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('PORT')))
