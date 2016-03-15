#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160315
#  @date          20160315
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


class Hello(Command):
    "prints hello world"

    def run(self):
        print "hello world"


COMMANDS = {
    'shell': Shell(make_context=make_shell_context),
    'hello': Hello(),
}
