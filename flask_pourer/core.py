# -*- coding: utf-8 -*-
'''
    core.py

    Contain major classes.
'''
import urlparse

import pymongo
from flask import current_app

# Warning: Should replace with our schema later
from marshmallow import Schema

from .decorators import jsonapi


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

    @classmethod
    @jsonapi
    def _create_obj(cls, obj_type):
        ''' Create object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _list_objs(cls, obj_type):
        ''' Get list of objects
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _get_obj(cls, obj_type, obj_id):
        ''' Get object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _get_obj_attr(cls, obj_type, obj_id, attr):
        ''' Get attribute of object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _get_obj_rels(cls, obj_type, obj_id, rel):
        ''' Get relationships of object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _update_obj(cls, obj_type, obj_id):
        ''' Update object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _update_obj_rels(cls, obj_type, obj_id, rel):
        ''' Update releationshops of object
        '''
        raise NotImplementedError()

    @classmethod
    @jsonapi
    def _remove_obj(cls, obj_type, obj_id):
        ''' Remove object
        '''
        raise NotImplementedError()

    def register(self, schema, url_prefix='/'):
        '''
            Register schema of object at url hook.

            :param schema:
                Definition of object
            :param url_prefix:
                URL prefix of url hook
        '''
        if issubclass(schema, Schema):
            obj_type = schema.__name__.lower()
            url_hook = urlparse.urljoin(url_prefix, schema.__name__.lower())

            # Fetching list of objects
            self.app.add_url_rule(
                url_hook,
                'list_obj',
                Pourer._list_objs,
                methods=['GET'],
                defaults={
                    'obj_type': obj_type,
                })

            # Fetching single object
            self.app.add_url_rule(
                url_hook + '/<obj_id>',
                'get_obj',
                Pourer._get_obj,
                methods=['GET'],
                defaults={
                    'obj_type': obj_type
                })

            # Fetching attribute of object
            self.app.add_url_rule(
                url_hook + '/<obj_id>/<attr>',
                'get_obj_attr',
                Pourer._get_obj_attr,
                methods=['GET'],
                defaults={
                    'obj_type': obj_type
                })

            # Fetching relationships of object
            self.app.add_url_rule(
                url_hook + '/<obj_id>/relationships/<rel>',
                'get_obj_rels',
                Pourer._get_obj_rels,
                methods=['GET'],
                defaults={
                    'obj_type': obj_type
                })

            # Create object
            self.app.add_url_rule(
                url_hook,
                'create_obj',
                Pourer._create_obj,
                methods=['POST'],
                defaults={
                    'obj_type': obj_type,
                })

            # Update object
            self.app.add_url_rule(
                url_hook + '/<obj_id>',
                'update_obj',
                Pourer._create_obj,
                methods=['PATCH'],
                defaults={
                    'obj_type': obj_type
                })

            # Update relationships of object
            self.app.add_url_rule(
                url_hook + '/<obj_id>/relationships/<rel>',
                'update_obj_rels',
                Pourer._update_obj_rels,
                methods=['PATCH'],
                defaults={
                    'obj_type': obj_type
                })

            # Delete object
            self.app.add_url_rule(
                url_hook + '/<obj_id>',
                'remove_obj',
                Pourer._remove_obj,
                methods=['DELETE'],
                defaults={
                    'obj_type': obj_type
                })

        else:
            raise ValueError('Invalid Schema: {}'.format(schema))
