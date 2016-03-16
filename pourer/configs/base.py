#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""BaseConfig
"""
import os

try:
    from .local import LocalConfig
except ImportError:
    raise ImportError("LocalConfig not imported")


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class FlaskConfig(object):
    """It's 0.10.1 of version for flask config

    Builtin Configuration Values:
        http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values
        http://docs.jinkan.org/docs/flask/config.html#id3
    """
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


class BaseConfig(LocalConfig, FlaskConfig):
    """Input your config of installed package in inheritance objects of BaseConfig
    """
