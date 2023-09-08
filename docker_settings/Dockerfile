FROM python:3.10-buster
LABEL author="ivanvic"
WORKDIR /app
COPY ../poetry.lock /app/
COPY ../pyproject.toml /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
RUN pip install gunicorn