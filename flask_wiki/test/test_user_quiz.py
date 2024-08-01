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


def test_quizresult(create_quiz, test_client):
    from wsgi import BASE_DIR
    import os
    import json
    from flask_wiki.models import QuizResults
    from flask import url_for

    with open(os.path.join(BASE_DIR, 'quiz_data.json'), 'r') as f:
        quiz_data = json.load(f)
    response = test_client.post('wiki/quiz_pass', json=quiz_data)
    assert response.status_code == 200
    quiz_id = quiz_data[0]['quiz_id']
    quiz_result = QuizResults.query.filter_by(quiz_id=quiz_id).one_or_none()
    assert quiz_result is not None
