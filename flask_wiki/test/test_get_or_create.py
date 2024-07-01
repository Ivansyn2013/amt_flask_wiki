from flask_wiki.models import Department
from db.init_db import db


def test_user_quiz_nums(init_database, create_quiz):
    user = init_database
    assert Department.query.all().count() == 0

    dep = Department.get_or_create(name='test_depart')
    db.session.add(dep)
    db.session.commit()

    assert Department.query.all().count() == 0
