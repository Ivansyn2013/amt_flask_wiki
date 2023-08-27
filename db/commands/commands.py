from dotenv import  load_dotenv
from flask import Blueprint
from db.init_db import db
import os
from flask_wiki.models import User
from sqlalchemy.exc import IntegrityError


cli_commands = Blueprint('cli_commands', __name__)

@cli_commands.cli.command("init-db")
def init_db():
    '''
    command for init flask db
    '''
    #db.drop_all()
    db.create_all()
    print('Db is inited')

@cli_commands.cli.command("create-admin")
def create_user():
    '''
    Cli command for create Flask user in db
    > Created admin: user
    '''

    admin = User(first_name='admin1', is_staff=True, login='admin')
    admin.password = os.getenv('FLASK_ADMIN_PASSWORD') or '123'
    db.session.add(admin)
    db.session.commit()
    print('Success user created: ', admin)

@cli_commands.cli.command("drop-db")
def drop_db():
    '''
    command for init flask db
    '''
    try:
        db.drop_all()

        db.engine.execute("DROP TABLE alembic_version")
        print('Db is droped')
    except IntegrityError as error:
        print(f'Error {error}')
