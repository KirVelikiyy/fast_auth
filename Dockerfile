FROM python:3.11

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt requirements.txt
COPY .env /app/.env

RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app
