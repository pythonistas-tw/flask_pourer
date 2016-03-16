#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160315
#  @date          20160315
#  @version       0.0
"""Command
"""
COMMANDS = {}


def install_commands():
    '''install_commands'''
    #
    from .auth_commands import AUTH_COMMANDS
    from .flask_commands import FLASK_COMMANDS

    #
    command_sets = (
        AUTH_COMMANDS,
        FLASK_COMMANDS,
    )

    #
    for commands in command_sets:
        COMMANDS.update(commands)

install_commands()
