FROM python:3.10-slim
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
