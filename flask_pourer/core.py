# -*- coding: utf-8 -*-
'''
    core.py

    Contain major classes.
'''
import pymongo
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Pourer(object):
    '''
        Collection of jsonapi objects.
    '''

    def __init__(self, app=None, mongo=None):
        '''
            Constructor.

            :param app:
                Flask application object
            :param mongo:
                Flask-PyMongo object
        '''
        self.app = app
        self.mongo = mongo
