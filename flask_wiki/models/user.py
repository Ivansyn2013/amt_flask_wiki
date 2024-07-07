from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY as p_Array
from sqlalchemy.orm import relationship, validates

from db.init_db import db
from flask_wiki.models import quiz
from security import flask_crypt


def _uuid_to_str():
    return str(uuid4())


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    _id = Column(String, primary_key=True, default=_uuid_to_str)
    first_name = Column(String(80), unique=False, nullable=False, default="",
                        server_default="")
    last_name = Column(String(80), unique=False, nullable=False, default="",
                       server_default="")
    login = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_validated = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    pages = relationship('PageDb', backref='creater', lazy='dynamic')

    # исправить
    _password = Column(LargeBinary, nullable=False, default=flask_crypt.generate_password_hash('123'))
    email = Column(String(255), nullable=False, default="", server_default="")
    # role = Column(String(200), nullable=True, default="", server_default="")
    USERS_ROLES = ["usual", "dep_chef", "all-seeing"]
    roles = Column(p_Array(String(50)), nullable=True)

    # Foreignkeys
    department_id = Column(String, ForeignKey('department._id'), nullable=True)
    # Many-to-many
    assigned_quizs = relationship('Quiz',
                                  secondary=quiz.quizs_users_relation_table,
                                  backref="users",
                                  lazy='dynamic',
                                  overlaps="assigned_to,quizzes")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_crypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_crypt.check_password_hash(self._password, password)

    @validates('roles')
    def validate_role(self, val, value_list: list):
        if not all(val in self.USERS_ROLES for val in value_list):
            raise ValueError(f"All values must be in {self.USERS_ROLES}")
        return value_list

    def get_id(self):
        return self._id

    def __str__(self):
        return f"{self.first_name!r}"
