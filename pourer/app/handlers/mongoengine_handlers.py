#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""handle for pymongo
"""
# level1: native python packages
# None

# level2: native web framework packages
from flask import jsonify

# level3: relative web framework plugins
# None

# level4: third-party packages
from mongoengine.errors import NotUniqueError

# level5: specify-project packages
from .. import app


__all__ = [
    "handle_not_unique_error",
    # "handle_noresultfound_exception",
]


@app.errorhandler(NotUniqueError)
def handle_not_unique_error(err):
    """Execute insert but the data has duplicate index

    It will return my custom error code and message.

    return example:
        {
            "error_code": 1001,
            "message": "The account is registered."
        }
    """
    return jsonify(err.data), 400


'''
@app.errorhandler(NoResultFound)
def handle_noresultfound_exception(err):
    """Execute query but it doesn't find the data

    return example:
        {
            "message": "Not Found"
        }
    """
    return jsonify({"message": "Not Found"}), 404
'''
