#
FROM python:3.9.4-slim

#
WORKDIR /app

#
COPY requirements.txt .

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#
RUN \
    apt update && \
    apt install -y gcc python3-dev libpq-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

#
COPY . .


