from db.init_db import db
from .user import _uuid_to_str
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, UUID, DateTime, TEXT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from security import flask_crypt
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quiz'
    _id = Column(String, primary_key=True, default=_uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow, editable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #Foreignkey
    created_by = Column(String, ForeignKey('user._id'), nullable=False)
    #One-to-many
    questions = relationship('QuizQuestion', backref='quiz', cascade='all, delete-orphan')

class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    _id = Column(String, primary_key=True, default=_uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    text = Column(TEXT, nullable=True)
    correct = Column(Boolean, nullable=True)

    #ForeignKey
    question_id = Column(String, ForeignKey('quiz_questions._id'), nullable=False)

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_quetions'
    _id = Column(String, primary_key=True, default=_uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    text = Column(TEXT, nullable=True)

    #Foreignkeys
    answers = relationship('QuizAnswer', backref='question', cascade='all, delete-orphan')
    quiz_id = Column(String, ForeignKey('quiz._id'), nullable=False)
