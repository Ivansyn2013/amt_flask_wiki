import os

import pytest
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from db.init_db import db
from examples.app import create_app
from flask_wiki.models import User, Quiz, QuizQuestion, QuizAnswer
from flask_wiki.my_options import get_obligatory_fields

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
    user_list = []

    with app.app_context():
        db.drop_all()
        db.create_all()

        for i in range(5):
            user_data = (
                f'test_user{i}',
                f'test_user_lastname{i}',
                f'test_user_login{i}',
                False,
                True,
                False,
            )

            user_data = dict(zip(user_fields, user_data))
            user = User(**user_data)
            User.password = '123'
            user_list.append(user)

        db.session.add_all(user_list)
        db.session.commit()
        yield user

@pytest.fixture
def create_quiz(init_database):
    user = init_database

    quiz_list = []
    for i in range(1,10):
        answer = QuizAnswer(text=f'TestAnswer{i}', correct=False)

        question = QuizQuestion(text=f'TestQuestion{i}', answers=[answer])

        quiz = Quiz(name=f'test_name{i}',
                    threshold=10,
                    created_by=user._id,
                    questions=[question],
                    assigned_to=[user],)
        quiz_list.append(quiz)

    db.session.add_all(quiz_list)
    db.session.commit()



