FROM python:3.9

WORKDIR /app

COPY . ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r venv/requirements.txt

ENV HOST 0.0.0.0
ENV PORT 80

CMD python3 -m pytest; uvicorn project.main:app --reload --host ${HOST} --port ${PORT}
