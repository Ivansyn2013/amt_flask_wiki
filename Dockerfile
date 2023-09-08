FROM ivanvic/amt_wiki_req:v1
WORKDIR /app
COPY . /app/
#RUN pip install poetry
#RUN poetry config virtualenvs.create false && poetry install \
#    --no-interaction --no-ansi
#RUN pip install gunicorn
RUN flask db migrate
RUN flask db upgrade
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5006"]
