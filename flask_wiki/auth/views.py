from flask import Blueprint, render_template, render_template_string
from flask_login import user_unauthorized, LoginManager
from flask_wiki.models import User

user_auth = Blueprint('user_auth',
                      __name__,
                      template_folder='templates',
                      static_folder='static',
                      )

login_manager = LoginManager()
login_manager.login_view = "user_auth.login"
login_manager.login_message = 'Привет'


@login_manager.user_loader
def get_user(user):
    return User.get(user)
@user_auth.route('/', endpoint='login')
def login():
    return render_template('wiki/login.html')

@user_auth.route('/registration/', endpoint='registration')
def registration():
    return render_template('wiki/registration.html')

@user_auth.route('/list/', endpoint='list')
def user_show():
    data = User.query.all()
    return render_template_string('{{ for user in users }}', users=data)
