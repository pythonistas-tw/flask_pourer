# -*- coding: utf-8 -*-
'''
    decorators.py

    Contain useful decorators for whole packages.
'''

from functools import wraps
from mimeparse import parse_mime_type
from flask import request, make_response, abort


def _validate_content_type(content_type):
    if content_type:
        mime_type, mime_subtype, mime_params = parse_mime_type(content_type)
        # Servers MUST respond with a 415 Unsupported Media Type status
        # code if a request specifies the header Content-Type:
        # application/vnd.api+json with any media type parameters.
        if mime_type == 'application' and mime_subtype == 'vnd.api+json':
            if mime_params:
                abort(415)


def _validate_accept(accept):
    valid_jsonapi = False
    invalid_jsonapi = False
    if accept:
        for media in [item.strip() for item in accept.split(',')]:
            media_type, media_subtype, media_params = parse_mime_type(media)
            if media_type == 'application' and media_subtype == 'vnd.api+json':
                media_params.pop("q", None)
                if media_params:
                    invalid_jsonapi = True
                else:
                    valid_jsonapi = True
        # Servers MUST respond with a 406 Not Acceptable status code if a
        # request's Accept header contains the JSON API media type and all
        # instances of that media type are modified with media type parameters.
        if invalid_jsonapi and not valid_jsonapi:
            abort(406)


def jsonapi(f):
    '''
        Confirm request & response compliance with jsonapi format
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Validate request before process
        _validate_content_type(request.headers.get('Content-Type'))
        _validate_accept(request.headers.get('accept'))

        response = make_response(f(*args, **kwargs))

        # Set Content-Type in response
        response.headers['Content-Type'] = 'application/vnd.api+json'

        return response
    return decorated_function
