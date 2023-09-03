from flask import (
    Blueprint,
    render_template,
    render_template_string,
    redirect,
    request,
    current_app,
    url_for, flash,
)
from flask_login import user_unauthorized, LoginManager, current_user, login_user, logout_user, login_required
from flask_wiki.models import User
from flask_wiki.auth.forms import RegistrationForm
from db.init_db import db
from sqlalchemy.exc import IntegrityError
from flask_wiki.auth.forms import LoginForm


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
    return User.query.get(user)


@user_auth.route('/', methods =['POST', "GET"], endpoint='login')
def login():
    if current_user.is_authenticated and current_user.is_validated:
        return redirect(url_for('wiki.index'))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).one_or_none()
        if user is None:
            flash(f"Такой пользователь не найден", "error")
            return render_template("auth/login.html", form=form,
                                   error="User name doen't exist")
        if not user.validate_password(form.password.data):
            flash(f"Неверный пароль", "error")
            return render_template("auth/login.html", form=form,
                                   error="invalid user name or password")

        login_user(user)
        flash(f"Добро пожаловать {user.first_name}", "success")
        return redirect(url_for('wiki.index'))
    return render_template("auth/login.html", form=form)


@user_auth.route('/registration/', methods=["POST", "GET"], endpoint='registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('wiki.index'))

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("Такой Email уже зарегистрирован")
            return render_template("auth/registration.html", form=form)

        if User.query.filter_by(login=form.login.data).count():
            form.login.errors.append("Пользователь уже существует")
            return render_template("auth/registration.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            login=form.login.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user")
            error = 'Could nor create user'
        else:
            current_app.logger.info(f'Create user {user}')
            login_user(user)
            flash(f"Пользователь {user.first_name} успешно зарегистирован", "info")
            return redirect(url_for('wiki.index'))
    return render_template('auth/registration.html', form=form, error=error)


@user_auth.route('/list/', endpoint='list')
def user_show():
    data = User.query.all()
    return render_template_string('{% for user in users %} {{ user }} {% endfor %}', users=data)

@user_auth.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    flash("Пользователь вышел", "success")
    return redirect(url_for("user_auth.login"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(_id=user_id).one_or_none()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("user_auth.login"))
