from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean, LargeBinary, ForeignKey, DateTime, Text, desc
from sqlalchemy.dialects.postgresql import ARRAY as p_Array
from sqlalchemy.orm import relationship, validates
from werkzeug.exceptions import NotFound

from flask_wiki.models import PageDb

from sqlalchemy import event
from db.init_db import db
from flask_wiki.models import quiz
from security import flask_crypt
from datetime import datetime

def _uuid_to_str():
    return str(uuid4())


class Review(db.Model):
    """Model of reviews on educations modules
    topic - title of page
    text - text of review (them)
    category - errors, notes, advice
    closed - status of review
    """

    __tablename__ = 'reviews'
    _id = Column(String, primary_key=True, default=_uuid_to_str)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    page_title = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    close_date = Column(DateTime, nullable=True)
    closed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey('user._id'), nullable=False)

    reviewer = relationship("User", back_populates="reviews")

    def get_page(self):
        """Return the last saved page with this title like in review page_title"""
        closest_page = (
            PageDb.query
            .filter_by(title=self.page_title)
            .order_by(desc(PageDb.created_at))
            .first()
        )

        if not closest_page:
            raise NotFound(f"No such page title: {self.page_title}")
        return closest_page

@event.listens_for(Review, 'before_update')
def set_close_date(mapper, connection, target):
    """Change close_date if review.closed = True"""
    if target.closed:
        target.close_date = datetime.now()
