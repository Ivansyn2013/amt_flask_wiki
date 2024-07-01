import logging

logger = logging.getLogger(__name__)


def create_quiz_from_request(data, user):
    '''Create a quiz question from a request form create_quiz view'''
    from flask_wiki.models import Quiz, QuizQuestion, QuizAnswer, Department
    logger.debug(data)
    questions = []
    try:
        for question_data in data['questions']:
            quest_text = question_data['text']
            answers = []
            for answer in question_data['answers']:
                answer = QuizAnswer(
                    text=answer['text'],
                    correct=answer['correct'],
                )
                answers.append(answer)
            question = QuizQuestion(text=quest_text, answers=answers)
            questions.append(question)

    except KeyError as e:
        logger.error('create_quiz_from_request function raise error\n' + e)
        return None

    departmet = Department.get_or_create(name=data['quiz_department']).first()
    quiz = Quiz(name=data['quiz_name'],
                threshold=data['quiz_threshold'],
                created_by=user._id,
                department_id=departmet._id,
                questions=questions)

    return quiz
