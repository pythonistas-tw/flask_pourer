#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160129
#  @date          20160129
#  @version       0.0
"""Users API
"""
from flask import Blueprint


users_bp = Blueprint('users', __name__)


def init_flask_blueprint():
    from . import auth, basic

init_flask_blueprint()
