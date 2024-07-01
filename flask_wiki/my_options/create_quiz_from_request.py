import logging

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
