from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from db.init_db import db
from flask_wiki.my_options import uuid_to_str


class Department(db.Model):
    __tablename__ = 'department'
    _id = Column(String, primary_key=True, default=uuid_to_str)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String, unique=True, nullable=False)

    #Foreignkeys
    users = relationship('User', backref='department')
    quiz = relationship('Quiz', backref='department')