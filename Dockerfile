FROM python:3.11-slim

LABEL \
    name="amt_wiki" \
    version="3.0.0" \
    description="Amt Wiki Application" \
    maintainer="titmouse"
# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Установка зависимостей Python
COPY . /app/
WORKDIR /app/
RUN poetry add psycopg2
RUN poetry install --without dev



