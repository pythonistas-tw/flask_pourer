#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160316
#  @date          20160316
#  @version       0.0
"""Command
"""
# level1: native python packages
# None

# level2: native web framework packages
# None

# level3: relative web framework plugins
from flask.ext.script import Command, Shell

# level4: third-party packages
# None

# level5: specify-project packages
from .. import app
from database.user.document import User
from database.token.document import Token


def make_shell_context():
    documents = {
        "User": User,
        "Token": Token
    }
    return dict(app=app, **documents)


FLASK_COMMANDS = {
    'shell': Shell(make_context=make_shell_context),
}
