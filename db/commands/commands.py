from dotenv import  load_dotenv
from flask import Blueprint
from db.init_db import db
import os
from flask_wiki.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text


cli_commands = Blueprint('cli_commands', __name__)

@cli_commands.cli.command("init-db")
def init_db():
    '''
    command for init flask db
    '''
    db.create_all()
    print('Db is inited')

@cli_commands.cli.command("create-admin")
def create_user():
    '''
    Cli command for create Flask user in db
    > Created admin: user
    '''

    admin = User(first_name='admin', is_staff=True, login='admin', is_validated=True, email='q@q.ru', is_admin=True)
    admin.password = os.getenv('FLASK_ADMIN_PASSWORD') or '123'
    db.session.add(admin)
    db.session.commit()
    print('Success user created: ', admin)

@cli_commands.cli.command("drop-db")
def drop_db():
    '''
    command for drop flask db
    '''
    try:
        db.reflect()
        db.drop_all()
        with db.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS alembic_version;"))

        print('Db is droped')
    except IntegrityError as error:
        print(f'Error {error}')
