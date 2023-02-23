import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import aioredis

# issue #1 if add project in import, docker compose will not run but tests will be passed
# if remove project in import docker compose will run but tests will give me an error that module db doesn't exist
from db.connections import get_db

# add env var from config.py
# same issue here with 'project import' project.config
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


# Error
# socket.gaierror: [Errno 8] nodename nor servname provided, or not known
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url('redis://redis')

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
