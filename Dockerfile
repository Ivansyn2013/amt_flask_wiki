FROM ivanvic/amt_wiki_req:v1
WORKDIR /app
COPY . /app/
#RUN pip install poetry
#RUN poetry config virtualenvs.create false && poetry install \
#    --no-interaction --no-ansi
#RUN pip install gunicorn
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
CMD ["gunicorn", "--workers=4", "wsgi:app", "-b", "0.0.0.0:5006"]
