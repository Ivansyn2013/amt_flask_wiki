from db.init_db import db
from flask_wiki.models import User, Quiz, QuizQuestion, QuizAnswer
from flask_wiki.my_options import get_obligatory_fields
from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger(__name__)

def test_user_creation(test_client, init_database):
    '''Тест на создание пользователя в базе , он созжается фикстурами'''
    user = User.query.first()
    assert user is not None
    assert user.first_name == 'test_user0'

def test_quiz_creation(test_client, init_database):
    '''Тест создания Опроса с вопросами и ответами'''
    user = init_database
    obliget_fields = get_obligatory_fields(Quiz)
    data = ('test_name', 10, user)
    quiz_data = dict(zip(obliget_fields, data))

    answer = QuizAnswer(text='TestAnswer', correct=False)

    question = QuizQuestion(text='TestQuestion', answers=[answer])

    quiz = Quiz(name='test_name',
                threshold=10,
                created_by=user._id,
                questions=[question])

    logger.info(quiz)

    db.session.add(quiz)
    db.session.commit()
    assert quiz is not None
    assert quiz.name == Quiz.query.first().name


