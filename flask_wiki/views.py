# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Views to respond to HTTP requests."""

import glob
import os
from functools import wraps

from babel import Locale
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for, jsonify)
from flask_babelex import gettext as _
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

from flask_wiki.models import PageDb, Quiz, QuizQuestion, QuizAnswer

from .api import Processor, current_wiki, get_wiki
from .forms import EditorForm, NewPageForm, CreateQuizForm
from db.init_db import db
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint(
    'wiki',
    __name__,
    template_folder='templates',
    static_folder='static'
)


# PERMISSIONS
# ===========
def can_read_permission(func):
    """Check Reading Permission."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        permission = current_app.config.get('WIKI_READ_VIEW_PERMISSION')()
        if isinstance(permission, bool):
            if not permission:
                abort(403)
            return func(*args, **kwargs)
        return permission
    return decorated_view


def can_edit_permission(func):
    """Check Edition Permission."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        #permission = current_app.config.get('WIKI_EDIT_VIEW_PERMISSION')()
        permission = current_user.is_authenticated and current_user.is_staff
        if isinstance(permission, bool):
            if not permission:
                abort(403)
            return func(*args, **kwargs)
        return permission
    return decorated_view


# FILTERS
# =======
@blueprint.app_template_filter()
def prune_url(path):
    return path.replace(
        current_app.config.get('WIKI_URL_PREFIX'),
        '').strip('/')


@blueprint.app_template_filter()
def translate_ln(ln):
    return Locale(current_wiki.current_language).languages.get(ln)


@blueprint.app_template_filter()
def edit_path_list(path):
    ln = path.split('_')[-1]
    base_path = path
    if ln in current_wiki.languages:
        base_path = path.rsplit('_', 1)[0]
    return list(
        filter(
            lambda v: v['path'] != path,
            [dict(ln=ln, path='_'.join((base_path, ln)))
             for ln in current_wiki.languages]))

@blueprint.app_template_filter()
def date_format(value, format=None):
    return value.strftime("%d-%m-%Y")

# PROCESSORS
# ==========
@blueprint.context_processor
def permission_processor():
    return dict(
        can_edit_wiki=current_app.config.get('WIKI_EDIT_UI_PERMISSION')(),
        can_read_wiki= current_app.config.get('WIKI_READ_UI_PERMISSION')()
    )


# MISCS
# =====
@blueprint.before_request
def setWiki():
    get_wiki()

@blueprint.before_request
def check_auth():
    if (not current_user.is_authenticated and request.endpoint != 'login'):
        flash("Доступ ограничен только для зарегистрированных пользователей")
        return redirect(url_for('user_auth.login'))
    if all((current_user.is_authenticated, not current_user.is_validated, request.endpoint != 'login',
            request.endpoint != '')):
        flash("Данный пользователь требует подтверждения администратора", 'warning')
        return redirect(url_for('user_auth.login'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config.get('WIKI_ALLOWED_EXTENSIONS')
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ROUTES
# ======
@blueprint.route('/')
@can_read_permission
def index():
    return redirect(url_for('wiki.page', url=current_app.config.get('WIKI_HOME')))


@blueprint.route('/<path:url>/')
@can_read_permission
def page(url):

    page = current_wiki.get_or_404(url)
    try:
        page_db = PageDb.query.filter_by(url=page.url).first()
        if not page_db:
            PageDb.save_in_db(page, current_user)
            page_db = PageDb.query.filter_by(url=page.url).first()

        files_urls = page_db.file_url.all()
    except Exception as error:
        current_app.logger.error(error)
        if type(error) is not AttributeError:
            flash('Ошибка подключения', 'error')
        files_urls = None

    return render_template(
        current_app.config.get('WIKI_PAGE_TEMPLATE'),
        page=page,
        files_urls=files_urls,
    )


@blueprint.route('/edit/<path:url>/', methods=['GET', 'POST'])
@can_edit_permission
def edit(url):
    page = current_wiki.get(url)
    #
    # print(page)
    #
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save(current_user)
        flash(_('Сохранено'), category='success')
        return redirect(url_for('wiki.page', url=url))
    return render_template(
        current_app.config.get('WIKI_EDITOR_TEMPLATE'),
        form=form, page=page, path=url)


@blueprint.route('/preview/', methods=['POST'])
@can_edit_permission
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'], data['toc'] = processor.process()
    return data['html']

@blueprint.route('/page/delete/<path:url>')
@can_edit_permission
def delete_page(url):
    if current_wiki.delete(url):
        flash(_('Page deleted'), category='success')
    else:
        flash(_('Could not delete page as it does not exist.'), category='error')
    return redirect(url_for('wiki.index'))

@blueprint.route('/file/delete/<path:filename>')
@can_edit_permission
def delete_file(filename):
    '''Удаление отключено'''
    abort(403)

    path = os.path.join(current_app.config.get('WIKI_UPLOAD_FOLDER'), filename)
    try:
        os.remove(path)
        flash(_('File deleted'), category='success')
    except Exception as e:
        flash(_('Something went wrong. Could not delete file.'), category='error')
    return redirect(url_for('wiki.files'))

@blueprint.route('/files', methods=['GET', 'POST'])
@can_edit_permission
def files():
    if request.method == 'POST' and current_app.config['WIKI_EDIT_UI_PERMISSION']():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(_('No file part'))
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash(_('No selected file'))
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            output_filename = os.path.join(
                current_app.config['WIKI_UPLOAD_FOLDER'], filename)
            if os.path.isfile(output_filename):
                flash(_('File already exists'), category='danger')
            else:
                file.save(output_filename)
    if request.method == 'POST' and not current_app.config['WIKI_EDIT_UI_PERMISSION']():
        flash(_('You do not have the permission to add files.'))
    files = [os.path.basename(f) for f in sorted(glob.glob(
        '/'.join([current_app.config.get('WIKI_UPLOAD_FOLDER'), '*'])), key=os.path.getmtime)]
    return render_template(
        current_app.config.get('WIKI_FILES_TEMPLATE'),
        files=files)


@blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = current_wiki.search(query)
    return render_template(
        current_app.config.get('WIKI_SEARCH_TEMPLATE'),
        results=results, query=query)


@blueprint.errorhandler(404)
def not_found(error):
    return render_template(
        current_app.config.get('WIKI_NOT_FOUND_TEMPLATE')), 404


@blueprint.errorhandler(403)
def forbidden(error):
    return render_template(
        current_app.config.get('WIKI_FORBIDDEN_TEMPLATE')), 403


@blueprint.route('/create_page', methods=['GET', 'POST'])
@can_read_permission
def create_page():
    if request.method == 'GET':
        return render_template('wiki/create_page.html')
    elif request.method == 'POST':
        form = NewPageForm(obj=request.args)
        pass

@blueprint.route('/list_pages', methods=['GET'])
@can_read_permission
def list_pages():
    '''Функция рисует список страниц, можно передать что-нить через реквест (request.args) и забрать по индексу'''
    r = current_wiki

    if 'page_tag' in request.args:
        page_tag = request.args['page_tag']
        list_pages = r.index_by_tag(page_tag)
    else:
        list_pages = r.index()

    return render_template('wiki/list_pages.html', list_pages=list_pages)

@blueprint.route('/video', methods=['GET'])
@can_read_permission
def video_player():
    videos = [os.path.basename(f) for f in sorted(glob.glob(
        '/'.join([current_app.config.get('WIKI_UPLOAD_FOLDER'), '*.mp4'])), key=os.path.getmtime)]
    return render_template('wiki/video_play.html', page=[], videos=videos)


@blueprint.route('/list_pages_by_moduls', methods=['GET'])
@can_read_permission
def list_pages_by_moduls():

    tag = 'модуль'
    r = current_wiki
    list_pages = r.index_by_tag(tag)
    return render_template('wiki/list_pages.html', list_pages=list_pages)

@blueprint.route('/show_quizzs', methods=['GET'])
@can_edit_permission
def show_quizzs():
    list_quizs = Quiz.query.all()
    return render_template('quiz/show_quizzs.html', list_quizs=list_quizs)

@blueprint.route('/create_q', methods=['GET', 'POST'])
@can_edit_permission
def create_quiz():
    '''View for quiz creating with form'''
    from flask_wiki.my_options import create_quiz_from_request
    from db.init_db import db
    import psycopg2

    form = CreateQuizForm()
    if request.method == 'GET':

        return render_template('quiz/create_quiz.html', form=form)

    elif request.method == 'POST': #and form.validate_on_submit():
        data = request.json
        if data['questions'] == {}:
            return abort(400, "Ошибка теста. Не может быть только один вопрос")

        user = current_user
        quiz = create_quiz_from_request(user=user, data=data)

        try:
            db.session.add(quiz)
            db.session.commit()
        except (SQLAlchemyError, psycopg2.errors.UniqueViolation) as e:
            logger.error(f"Error to write in db {quiz}\n{e}")
            db.session.rollback()
            if "duplicate key value " in str(e):
                flash('Такой тест уже существует', category='info')
                return render_template('quiz/quiz_details.html', quiz=quiz)

            return abort(400, "Ошибка записи теста")

        return render_template('quiz/quiz_details.html', quiz=quiz)


@blueprint.route('/myquiz', methods=['GET'])
@can_edit_permission
def my_quizs():
    '''Show assigned quizs'''
    from flask_wiki.models import User
    user = current_user
    list_quizs = Quiz.query.join(Quiz.assigned_to).filter(User._id == user._id)
    return render_template('quiz/my_quizzs.html', list_quizs=list_quizs)

@blueprint.route('/quiz/<quiz_id>', methods=['GET'])
@can_edit_permission
def quiz_details(quiz_id):
    from sqlalchemy.orm import joinedload

    quiz = (Quiz.query.options(
        joinedload(Quiz.assigned_to),
        joinedload(Quiz.created_by_user))
            .get(quiz_id))
    if not quiz:
        return abort(404, "Тест не найден")
    return render_template('quiz/quiz_details.html', quiz=quiz)


@blueprint.route('/assinged/<quiz_id>', methods=['GET', 'POST'])
@can_edit_permission
def assinged_user_list(quiz_id):
    from flask_wiki.models import User
    from flask_wiki.my_options import assined_quiz_to_users
    if request.method == 'GET':
        users = User.query.all()
        return render_template('quiz/assinged_to.html', users=users, quiz_id=quiz_id)

    else:
        data = request.form
        data_dict = dict(data.lists())

        if assined_quiz_to_users(**data_dict):
            flash("Пользователи успешно подписаны", category='info')
            return redirect(url_for('wiki.index'))
        else:
            flash("Произошла ошибка назначения пользователей", category='danger')
            return redirect(url_for('wiki.index'))
@blueprint.route('/quiz_play/<quiz_id>', methods=['GET', 'POST'])
@can_read_permission
def quiz_play(quiz_id):
    from sqlalchemy.orm import joinedload
    quiz = Quiz.query.options(joinedload(Quiz.questions)).get_or_404(quiz_id)
    quiz_dict = quiz.to_dict()

    return render_template('quiz/quiz_play.html', quiz=quiz_dict)

@blueprint.route('/quiz_pass/', methods=['POST'])
def quiz_get_result():
    from flask_wiki.models import QuizResults, QuestonAnswerResult
    data = request.json[0]

    try:
        quiz_results = QuizResults(
            user_id=current_user._id,
            quiz_id=data['quiz_id'],
        )
        db.session.add(quiz_results)
        db.session.commit()

        result_table = QuestonAnswerResult(
            question_id=data['question_id'],
            answer_id=data['answer_id'],
            correct=data['correct'],
            quiz_result_id=quiz_results._id,
        )
        db.session.add(result_table)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error wtite in db quize results\n{e}")
        return jsonify(500, "Error wtite in db quize results")

    quiz = Quiz.query.get(data['quiz_id'])
    print()
    #current_user.assigned_quizs.filter(Quiz._id == quiz._id).delete()
    # нужно удалить запись из назначенных
    return jsonify(200, 'OK')

@blueprint.route('/quiz/show_results', methods=['GET'])
@can_edit_permission
def show_results():
    from flask_wiki.models import User, QuizResults
    users = User.query.join(QuizResults)
    results = QuizResults.query.join(User).filter(QuizResults.user_id == User._id).all()

    return render_template("quiz/show_quiz_results.html", users=users, results=results)

@blueprint.route('/quiz/result_details/<result_id>', methods=['GET'])
@can_edit_permission
def result_details(result_id):
    from flask_wiki.models import User, QuizResults, QuestonAnswerResult

    res = QuestonAnswerResult.query.join(QuizResults).filter(QuizResults._id == result_id).all()
    return render_template("quiz/result_details.html",
                           question=res,
                           )
