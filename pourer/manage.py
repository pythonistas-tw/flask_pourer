#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""manage.py
"""
from flask.ext.script import Manager

from app import FlaskApplicationFactory
import configs
import scripts


app = FlaskApplicationFactory().create_app(configs.CONFIGS['development'])
manager = Manager(app)


if __name__ == "__main__":
    manager.run(scripts.COMMANDS)
