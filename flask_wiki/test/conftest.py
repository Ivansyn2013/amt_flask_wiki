from flask_sqlalchemy import SQLAlchemy
from db.init_db import db
import pytest
from flask_wiki.my_options import get_obligatory_fields
from flask_wiki.models import PageDb, FilesUrls
from flask_wiki.models import User
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from examples.app import create_app

load_dotenv('../../.env')
DB = os.getenv('PGDB_TEST')
USER = os.getenv('PGUSER')
PASS = os.getenv('PGPASSWORD')
PORT = os.getenv('PGPORT')

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost:5433/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    db = SQLAlchemy()
    app = create_app(test_config='test_mode')

@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_config='test_mode')

    testing_client = app.test_client()

    with app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    app = create_app(test_config='test_mode')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASS}@localhost:{PORT}/{DB}'

    user_fields = get_obligatory_fields(User)
    user_fields.remove('_password')
    user_data = (
        'test_user',
        'test_user_lastname',
        'test_user_login',
        False,
        True,
        False,
                 )
    user_data = dict(zip(user_fields, user_data))

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(**user_data)
        User.password = '123'
        db.session.add(user)
        db.session.commit()
        yield user


