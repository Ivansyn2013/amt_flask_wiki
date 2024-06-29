from flask_wiki.models import Quiz, User


def test_user_quiz_nums(init_database, create_quiz):
    user = init_database
    quiz_nums = Quiz.query.join(Quiz.assigned_to).filter(User._id == user._id).count()
    assert quiz_nums == 9