from logging import getLogger
from urllib.parse import unquote  # для декодированяи кириллицы

from flask import (
    Blueprint,
    render_template,
    render_template_string,
    redirect,
    request,
    current_app,
    url_for,
    flash,
    jsonify
)
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from db.init_db import db
from flask_wiki.auth.forms import LoginForm
from flask_wiki.auth.forms import RegistrationForm
from flask_wiki.models import PageDb, FilesUrls
from flask_wiki.models import User
from flask_wiki.my_options.delete_fileurl_from_db import delete_fileurl_from_db, find_page_in_db

user_auth = Blueprint('user_auth',
                      __name__,
                      template_folder='templates',
                      static_folder='static',
                      )

login_manager = LoginManager()
login_manager.login_view = "user_auth.login"
login_manager.login_message = 'Привет'

s3_logger = getLogger('s3_logger')


@login_manager.user_loader
def get_user(user):
    return User.query.get(user)


@user_auth.route('/', methods=['POST', "GET"], endpoint='login')
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


@user_auth.route("/upload_files/", methods=['POST'], endpoint="upload_files")
@login_required
def upload_files():
    '''Функция для загрузуки виддео в хранилище'''
    from flask_wiki.my_options import allowed_file, create_client, BUCKET
    from dotenv import load_dotenv
    import os

    load_dotenv()

    if 'file' not in request.files:
        flash('Не найден фаил', 'warning')
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']

    if file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        page_name = request.headers['pagename']
        decode_page_name = unquote(page_name, encoding='utf-8')
        PATH = f'{os.getenv("PATH_S3_DIR")}/{decode_page_name}/{filename}'
        file_obj = request.files.get('file')
        # Generate a presigned URL for S3 upload

        s3 = create_client()
        # создание ссылки для загрузки
        # presigned_url = s3.generate_presigned_url(
        #     'put_object',
        #     Params={'Bucket': BUCKET, 'Key': filename},
        #     ExpiresIn=360  # The URL will expire in 1 hour
        # )

        try:
            s3.put_object(Bucket=BUCKET, Key=PATH, Body=file_obj)

            flash('Создана ссылка', "success")
            file_url = f'{s3.meta.endpoint_url}/{BUCKET}/{PATH}'  # полная ссылка

            db_page = PageDb.query.filter_by(url=decode_page_name).first()
            file_url_db = FilesUrls(file_name=filename, file_url=file_url)
            db_page.file_url.append(file_url_db)
            db.session.add(db_page)
            db.session.commit()

            s3_logger.info(f'Сохранен фаил в хранилище с именем {PATH} и ссылкой {file_url}')


        except Exception as e:
            print(e)
            flash('Ошибка загрузки файла', "warning")
            return jsonify({'success': False, 'error': str(e)})

        return jsonify({'success': True})

    return jsonify({'error': 'Ошибка имени файла'})


@user_auth.route("/remove_files/", methods=['POST'], endpoint="remove_files")
@login_required
def remove_files():
    ''' Функция удаления файла из S3'''
    from flask_wiki.my_options import create_client, BUCKET
    from dotenv import load_dotenv
    import os

    load_dotenv()

    if request.method == 'POST' and request.headers.get("remove_file"):
        pagename = unquote(request.headers.get('pagename'), encoding='utf-8')
        file_name = unquote(request.headers.get("remove_file"), encoding='utf-8')
        PATH = f'{os.getenv("PATH_S3_DIR")}/{file_name}'
        db_page = find_page_in_db(pagename)

        try:
            s3 = create_client()
            result = s3.delete_object(Bucket=BUCKET, Key=PATH)
            status = result['ResponseMetadata']['HTTPStatusCode']
            s3_logger.info(f'Выполнен запрос на удаление файла = {file_name} Код ответа = {status}')
            if status != 200:
                s3_logger.warning(f'Фаил не найден в хранилище! Ссылка будет удалена! \n '
                                  f'Файл = {file_name} Код ответа = {status}')
        except Exception as e:
            s3_logger.error(f'Не удалось удалить фаил {e}')
            flash('Ошибка удаления файла', 'error')
            return jsonify({'message': 'Ошибка удаления файла'})

        delete_result_db = delete_fileurl_from_db(db_page, file_name)
        return delete_result_db

    return jsonify({'message': 'Нет файла'})
