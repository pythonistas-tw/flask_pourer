#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160315
#  @date          20160315
#  @version       0.0
"""decorators
"""
# level1: native python packages
from functools import wraps

# level2: native web framework packages
from flask import g, request, abort

# level3: relative web framework plugins
# None

# level4: third-party packages
# None

# level5: specify-project packages
from database.token.document import Token


def token_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # request process: get key from Authorization
        key = request.headers.get('Authorization', '')
        if not key:
            abort(401)

        # model process: get token by key
        token = Token.objects.filter(key=key).first()
        if not token:
            abort(401)

        # request process: store token in request
        request.authorization = token
        return f(*args, **kwargs)
    return decorated_function

