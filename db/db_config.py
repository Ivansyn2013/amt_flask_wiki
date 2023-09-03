class DbConfig(object):
    TESTING = False
    WTF_CSRF_ENABLED = True
    FLASK_ADMIN_SWATCH = 'admin'

class Develop(DbConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.db'
    SQLALCHEMY_MODIFICATIONS = False
    SECRET_KEY = 'abcdefg123456'
    # Flask-admin
    # =============
    FLASK_ADMIN_SWATCH = 'cerulean'