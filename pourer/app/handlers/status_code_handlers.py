#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""handle for status code
"""
# level1: native python packages
# None

# level2: native web framework packages
from flask import jsonify

# level3: relative web framework plugins
# None

# level4: third-party packages
# None

# level5: specify-project packages
from .. import app


__all__ = [
    "handle_notfound",  # 404
    "handle_unauthorized",  # 401
    "handle_unprocessable_entity_from_webargs",  # 422
]


@app.errorhandler(404)
def handle_notfound(err):
    """It's possible to be caused by url or sqlalchemy
    """
    return jsonify({"message": "Not Found"}), 404


@app.errorhandler(401)
def handle_unauthorized(err):
    """It's possible to be caused by login
    """
    return jsonify({"message": "Unauthorized"}), 401


@app.errorhandler(422)
def handle_unprocessable_entity_from_webargs(err):
    """unprocessable_entity_from_webargs
    """
    msgs = {k: v.pop() for k, v in err.data['messages'].items()}
    return jsonify({
        'message': "Invalid request could not be understood "
                   "by the server due to malformed syntax.",
        'errors': msgs,
    }), 400
    return jsonify(res_data), 400
