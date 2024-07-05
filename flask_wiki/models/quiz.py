from db.init_db import db
from flask_wiki.my_options import uuid_to_str
from sqlalchemy import (event,
                        Column,
                        Integer,
                        String,
                        Boolean,
                        LargeBinary,
                        ForeignKey,
                        UUID,
                        DateTime,
                        TEXT,
                        )
from sqlalchemy.orm import relationship
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_wiki.models.departments import Department

quizs_users_relation_table = db.Table('quizs_users_relation_table',
                                      db.Column('quiz_id', String, db.ForeignKey('quiz._id')),
                                      db.Column('user_id', String, db.ForeignKey('user._id'))
                                      )


class Quiz(db.Model):
    '''
    created_at - создан кем, задается однажды
    updated_at - создан когда, задается однажды
    name - название теста
    threshold - порог прохождения
    department - отдел, из модели отделов О-М
    created_by - кем создан, из модели пользователей О-М
    update_by - кем обновлен, из модели пользователей О-М
    assigned_to - кому назначен, из модели пользователей М-М
    questions - вопросы теста, из модели тестов М-О
    url - url страницы для сдачи теста
    department - отдел компании
    '''
    __tablename__ = 'quiz'
    _id = Column(String, primary_key=True, default=uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    name = Column(String, unique=True, nullable=False)
    threshold = Column(Integer, nullable=False)
    url = Column(String, nullable=True)

    # Foreignkey

    created_by = Column(String, ForeignKey('user._id'),
                        nullable=False,
                        )
    # очень долго разбирался в рещультате такая конструкция позволяет
    # подгуржать данные и передавать в шаблон created_by_userс view quiz_details
    created_by_user = db.relationship('User', foreign_keys=[created_by],
                                      # back_populates='created_quizs',
                                      primaryjoin="User._id == Quiz.created_by")
    update_by = Column(String, ForeignKey('user._id'), nullable=True, default=None)

    # Many-to-Many
    assigned_to = relationship('User',
                               secondary=quizs_users_relation_table,
                               backref="quizzes",
                               overlaps="assigned_to,quizzes")

    # One-to-many
    questions = relationship('QuizQuestion',
                             backref='quiz',
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    department_id = Column(String, ForeignKey('department._id'), nullable=True)

    def to_dict(self):
        result = {}
        # result = {collunm.name: getattr(self, collunm.name) for collunm in self.__table__.columns}
        result["id"] = self._id
        result["name"] = self.name

        result["questions"] = [
            {"question": q.text,
             "question_id": q._id,
             "answer": [
                 {"answer_id": a._id,
                  "text": a.text,
                  "correct": a.correct}
                 for a in q.answers]
             }
            for q in self.questions
        ]

        return result

    def __repr__(self):
        return '<Quiz(id={0._id}, name={0.name})>'.format(self)


class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'

    _id = Column(String, primary_key=True, default=uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    text = Column(TEXT, nullable=False)
    correct = Column(Boolean, nullable=False, default=False)

    # ForeignKey O-M
    question_id = Column(String, ForeignKey('quiz_questions._id'), nullable=False)


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    _id = Column(String, primary_key=True, default=uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    text = Column(TEXT, nullable=False)

    # Foreignkeys
    quiz_id = Column(String, ForeignKey('quiz._id'), nullable=False)
    answers = relationship('QuizAnswer',
                           backref='question',
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    def __repr__(self):
        return 'QuizQuestion(id={0._id})'.format(self)


class QuizResults(db.Model):
    __tablename__ = 'quiz_results'
    _id = Column(String, primary_key=True, default=uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    travel_time = Column(Integer, nullable=True)
    result = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    # Foreign keys
    user_id = Column(String, ForeignKey('user._id'), nullable=False)
    quiz_id = Column(String, ForeignKey('quiz._id'), nullable=False)


class QuestonAnswerResult(db.Model):
    """Table for save ques-qnswer pairs for result of quiz
    TODO: Нашео ошибку. Модель выдает конкретные вопросы и ответы,
    а подразумевались их списки, относитлеьно конкретного квизз возмоно
    надо будет по другой таблице полазить"""

    __tablename__ = 'question_answer_results'
    _id = Column(String, primary_key=True, default=uuid_to_str)

    quiz_result_id = Column(String, ForeignKey('quiz_results._id'), nullable=False)

    question_id = Column(String, ForeignKey('quiz_questions._id'), nullable=False)
    answer_id = Column(String, ForeignKey('quiz_answers._id'), nullable=False)
    correct = Column(Boolean, nullable=False)

    # Relationships
    question_instance = relationship("QuizQuestion",  # for get inctanse not a just id
                                     lazy="joined",
                                     foreign_keys=[question_id])

    answer_instance = relationship("QuizAnswer",  # for get inctanse not a just id
                                   # lazy="joined",
                                   foreign_keys=[answer_id])
