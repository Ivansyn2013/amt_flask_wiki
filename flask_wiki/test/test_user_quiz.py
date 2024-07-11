from db.init_db import db
from flask_wiki.models import Quiz, User


def test_user_quiz_nums(init_database, create_quiz):
    user = init_database
    quiz_nums = Quiz.query.join(Quiz.assigned_to).filter(User._id == user._id).count()
    assert quiz_nums == 9


def test_quiz_assigned_delete(init_database):
    user = init_database
    all_quizs = len(Quiz.query.all())
    quiz_list = user.assigned_quizs.all()

    quiz = quiz_list[0]
    user.assigned_quizs.remove(quiz)
    db.session.commit()

    change_all_quizs = len(Quiz.query.all())
    assert len(user.assigned_quizs.all()) == len(quiz_list) - 1
    assert change_all_quizs == all_quizs


def test_quizresult(init_database):
    user = init_database
    pass
