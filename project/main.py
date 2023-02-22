import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# add environment variables
load_dotenv('../venv/.env')

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

@app.get('/')
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('PORT')))
