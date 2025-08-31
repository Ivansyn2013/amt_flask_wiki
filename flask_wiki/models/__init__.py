from flask_wiki.models.user import User
from .page import PageDb
from .files_urls import FilesUrls
from .quiz import (Quiz,
                   quizs_users_relation_table,
                   QuizAnswer,
                   QuizResults,
                   QuizQuestion,
                   # Department,
                   QuestionAnswerResult)
__all__ = [
    'User',
    'FilesUrls',
    'PageDb',
    'Quiz',
    'QuizAnswer',
    'QuizResults',
    'QuizQuestion',
    # 'Department',
    'QuestionAnswerResult',
    'quizs_users_relation_table',
]