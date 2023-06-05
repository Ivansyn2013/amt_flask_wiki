FROM python:3.10-buster
WORKDIR /app
COPY . /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install \
    --no-interaction --no-ansi
RUN pip install gunicorn
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5005"]
