FROM python:3.9

WORKDIR /app

COPY venv/requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

