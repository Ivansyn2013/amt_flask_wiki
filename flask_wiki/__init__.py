# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""This extension create a wiki from a tree directory."""

from flask import current_app
import os
from .views import blueprint
from werkzeug.middleware.shared_data import SharedDataMiddleware
from . import config
from flask_migrate import Migrate
from flask_wiki.auth.views import user_auth
from db.commands.commands import cli_commands
from db.init_db import db


class Wiki(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.register_blueprint(
            blueprint,
            url_prefix=app.config.get('WIKI_URL_PREFIX')
        )
        app.register_blueprint(
            user_auth,
        )
        app.register_blueprint(
            cli_commands,
        )
        app.add_url_rule(
            app.config.get('WIKI_URL_PREFIX') + '/files/<filename>',
            'uploaded_files', build_only=True)

        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {app.config.get(
            'WIKI_URL_PREFIX') + '/files': app.config['WIKI_UPLOAD_FOLDER']})
        app.extensions['flask-wiki'] = self

        migrate = Migrate(app, db, compare_type=True)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('WIKI_'):
                app.config.setdefault(k, getattr(config, k))
