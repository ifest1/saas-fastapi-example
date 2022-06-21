# Set base image
FROM python:3.9.4-slim

# Set workdir
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# Install packages
RUN pip install -U pip && \
    apt update && \
    apt install -y curl netcat && \
    apt install -y gcc python3-dev libpq-dev && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:/root/.poetry/bin"

# Copy API code
COPY . .

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi