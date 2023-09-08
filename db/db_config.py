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

class Deploy(DbConfig):
    from dotenv import load_dotenv
    import os

    load_dotenv()
    PGUSER = os.environ.get("PGUSER")
    PGPASSWORD = os.environ.get("PGPASSWORD")
    PGHOST = os.environ.get("PGHOST")
    PGDB = os.environ.get('PGDB')

    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDB}'
    SQLALCHEMY_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
