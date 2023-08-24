from db.init_db import db
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, UUID
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from security import flask_crypt
from uuid import uuid4


class User(UserMixin):
    class User(db.Model, UserMixin):
        _id = Column(UUID, primary_key=True, default=uuid4())
        first_name = Column(String(80), unique=False, nullable=False, default="",
                            server_default="")
        last_name = Column(String(80), unique=False, nullable=False, default="",
                           server_default="")
        login = Column(String(80), unique=False, nullable=False, default="",
                       server_default="")
        is_staff = Column(Boolean, nullable=False, default=False)
        is_validated = Column(Boolean, nullable=False, default=False)
        _password = Column(LargeBinary, nullable=True)
        email = Column(String(255), nullable=False, default="", server_default="")

        @property
        def password(self):
            return self._password

        @password.setter
        def password(self, value):
            self._password = flask_crypt.generate_password_hash(value)

        def validate_password(self, password) -> bool:
            return flask_crypt.check_password_hash(self._password, password)

        def __repr__(self):
            return f"< User {self.id} {self.first_name!r} {self.last_name}>"
