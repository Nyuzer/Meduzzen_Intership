import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI

# add environment variables
load_dotenv('../venv/.env')

app = FastAPI()


@app.get('/')
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('PORT')))
