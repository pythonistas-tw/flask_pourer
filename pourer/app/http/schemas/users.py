#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""marshmallow class
"""
# level1: native python packages
# None

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
from marshmallow_mongoengine import ModelSchema, fields

# level5: specify-project packages
from database.user.document import User


class UserSchema(ModelSchema):

    class Meta:
        model = User
        model_fields_kwargs = {'password': {'load_only': True}}
