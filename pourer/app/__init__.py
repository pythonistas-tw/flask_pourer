#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""Init flask app
"""
# level1: native python packages
# None

# level2: native web framework packages
from flask import Flask

# level3: relative web framework plugins
from flask.ext.mongoengine import MongoEngine

# level4: third-party packages
# None

# level5: specify-project packages
# None


app = Flask(__name__)


class FlaskApplicationFactory(object):
    '''FlaskApplicationFactory'''

    def install_extension(self):
        '''install_extension'''
        _ = MongoEngine(app)

    def install_blueprint(self):
        '''install_blueprint'''
        # Blueprint source: Import the blueprints and note these sources
        from .http.controllers import users

        # Blueprint List: Wrap up the all blueprints
        buleprints = (
            dict(blueprint=users.users_bp, url_prefix='/users'),
        )

        # Initializing process: Start to initial each blueprint
        for blueprint in buleprints:
            app.register_blueprint(**blueprint)

    def install_handlers(self):
        from .handlers import (
            status_code_handlers,
            mongoengine_handlers
        )

    def create_app(self, config_filename):
        '''create_app'''
        app.config.from_object(config_filename)
        self.install_extension()
        self.install_blueprint()
        self.install_handlers()
        return app
