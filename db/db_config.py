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
    load_dotenv('../.env_local')

    PGUSER = os.environ.get("PGUSER")
    PGPASSWORD = os.environ.get("PGPASSWORD")
    PGHOST = os.environ.get("PGHOST")
    PGDB = os.environ.get('PGDB')

    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    FLASK_DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDB}'
    SQLALCHEMY_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PORT = os.environ.get("PORT")
    FLASK_ADMIN_SWATCH = 'cerulean'

class Test_config(DbConfig):
    from dotenv import load_dotenv
    import os
    load_dotenv()

    PGUSER = os.environ.get("PGUSER")
    PGPASSWORD = os.environ.get("PGPASSWORD")
    PGHOST = os.environ.get("PGTESTHOST")
    PGDB = os.environ.get('PGDB')
    PORT = os.environ.get("PGPORT")

    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PORT}/{PGDB}'
    SQLALCHEMY_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ADMIN_SWATCH = 'cerulean'
