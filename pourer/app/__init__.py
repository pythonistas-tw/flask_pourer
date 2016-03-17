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


def url(blueprints, version=None):
    # data process: Decide url structure of the application
    prefix = '/%s' % version if version else ''

    # data process: set the new url_prefix (create new object and avoid mutable dict)
    bps = []
    for blueprint in blueprints:
        bps.append({
            'blueprint': blueprint['blueprint'],
            'url_prefix': prefix + blueprint['url_prefix']
        })
    return bps


class FlaskApplicationFactory(object):
    '''FlaskApplicationFactory'''

    def install_extension(self):
        '''install_extension'''
        _ = MongoEngine(app)

    def install_blueprint(self):
        '''install_blueprint'''
        # blueprint porcess: import patterns it's ready to be registered
        from .http.blueprints import BLUEPRINT_PATTERNS as http_bp_patterns

        # blueprint porcess: Add version for each patterns
        versioning_patterns = (
            url(http_bp_patterns),
            url(http_bp_patterns, version='v1'),
        )

        # blueprint porcess: app register blueprint
        for blueprint_patterns in versioning_patterns:
            for blueprint in blueprint_patterns:
                app.register_blueprint(**blueprint)

    def install_handlers(self):
        '''install_handlers'''
        from .handlers import (
            status_code_handlers,
            mongoengine_handlers
        )

    def install_middlewares(self):
        from .middlewares import process_request

    def create_app(self, config_filename):
        '''create_app'''
        app.config.from_object(config_filename)
        self.install_middlewares()
        self.install_extension()
        self.install_blueprint()
        self.install_handlers()
        return app
