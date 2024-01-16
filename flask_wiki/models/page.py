import sqlalchemy.exc

from flask_wiki.models.user import _uuid_to_str
from db.init_db import db
from sqlalchemy import Column,  String, Boolean, LargeBinary, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
class PageDb(db.Model):
    __tablename__ = "pages"

    _id = Column(String, primary_key=True, default=_uuid_to_str)

    title = Column(String, unique=True)
    html = Column(Text)
    tags = Column(String)
    create_date = Column(DateTime, default=datetime.now, server_default=func.now())
    update_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    body = Column(Text)
    content = Column(String)
    path = Column(String)
    url = Column(String)
    toc = Column(String)
    meta = Column(String)

    '''
    images - list - foreign key many to many
    videos - list - foreygn key'''
    #foreign keys
    creater =[]
    file_url = db.relationship('FilesUrls', backref='page', lazy='dynamic')

    @staticmethod
    def save_in_db(page):
        page_in_db = PageDb()
        for sett in dir(page):
            if sett in dir(page_in_db) and not sett.startswith('__'):
            #требуется преобразовагние типов
                if not type(getattr(page, sett)) in (str, datetime):
                    setattr(page_in_db, sett, 'None')
                else:
                    setattr(page_in_db, sett, getattr(page, sett))

        try:
            db.session.add(page_in_db)
            db.session.commit()
            return True
        except sqlalchemy.exc.SQLAlchemyError as error:
            print(error)
            return False





