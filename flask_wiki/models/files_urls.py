import sqlalchemy.exc

from flask_wiki.models.user import _uuid_to_str
from db.init_db import db
from sqlalchemy import Column,  String, Boolean, LargeBinary, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .page import PageDb

class FilesUrls(db.Model):
    __tablename__ = 'file_urls'

    _id = Column(String, primary_key=True, default=_uuid_to_str)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    #  ForeignKey
    page_id = db.Column(String, db.ForeignKey('pages._id'), nullable=False)

    def __str__(self):
        return str(self.file_url)