import logging

from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def create_quiz_from_request(data, user):
    '''Create a quiz question from a request form create_quiz view'''
    from flask_wiki.models import Quiz, QuizQuestion, QuizAnswer, Department

    logger.debug(data)
    questions = []
    try:
        for question_key, question_data in data['questions'].items():
            quest_text = question_data['text']
            answers = []
            for answer_key, answer_data in question_data['answers'].items():
                answer = QuizAnswer(
                    text=answer_data['text'],
                    correct=True if answer_data['correct'] == 1 else False,
                )
                answers.append(answer)
            question = QuizQuestion(text=quest_text, answers=answers)
            questions.append(question)

    except KeyError as e:
        logger.error('create_quiz_from_request function raise error\n' + e)
        return None

    departmet, status = Department.get_or_create(name=data['quiz_department'])
    quiz = Quiz(name=data['quiz_name'],
                threshold=data['quiz_threshold'],
                created_by=user._id,
                department_id=departmet._id,
                questions=questions)

    return quiz

def assined_quiz_to_users(**kwargs):
    '''Function for assinged users to quizs
    return True if ok and Fasle if not
    '''
    from db.init_db import db
    from flask_wiki.models import Quiz, User
    try:
        quiz = Quiz.query.get(kwargs['quiz_id'])
        users = User.query.filter(User._id.in_(kwargs['user'])).all()
        for user in users:
            if check_assigned(user, quiz):
                users.remove(user)

        quiz.assigned_to.extend(users)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f'Error in write assinged users. Function assined_quiz_to_users\n {e} ')
        return False

    return True

def check_assigned(user, quiz):
    '''Check is user already have this test'''
    from flask_wiki.models import Quiz, User
    #User.query.join(user.assigned_quizs).filter(quiz._id == Quiz._id).all()
    if quiz in user.assigned_quizs:
        return True
    else:
        return False
