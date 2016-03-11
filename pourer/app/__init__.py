#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""Init flask app
"""
from flask import Flask
from flask.ext.mongoengine import MongoEngine


class FlaskApplicationFactory(object):
    '''FlaskApplicationFactory'''
    app = Flask(__name__)

    def install_extension(self):
        '''install_extension'''
        _ = MongoEngine(self.app)

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
            self.app.register_blueprint(**blueprint)

    def install_handlers(self):
        pass

    def create_app(self, config_filename):
        '''create_app'''
        self.app.config.from_object(config_filename)
        self.install_extension()
        self.install_blueprint()
        self.install_handlers()
        return self.app
