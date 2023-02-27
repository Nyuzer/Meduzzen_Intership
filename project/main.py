import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import aioredis

from db.connections import get_db, get_redis

import config

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


@app.on_event("startup")
async def startup():
    redis = await get_redis()

    database = get_db()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    database = get_db()
    await database.disconnect()


@app.get('/')
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=int(config.PORT))
