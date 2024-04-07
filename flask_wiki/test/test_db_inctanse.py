
from examples.app import app
from db.init_db import db
import pytest
from flask_wiki.models import PageDb, FilesUrls
from db.db_config import Develop

@pytest.fixture
def client():
    #app.config.from_object(Develop)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client


def test_db_inctanse_creation(client):
    file = FilesUrls(file_name="test.txt", file_url="http://")
    page = PageDb(title="test", file_url=[file])
    with app.app_context():
        db.session.add(page)
        db.session.commit()

        page = PageDb.query.all()[-1]
        assert page.title == "test"
        assert str(page.file_url.all()[-1]) == "http://"
