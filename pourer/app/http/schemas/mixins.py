#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""mixin for marshmallow
"""
# level1: native python packages
# None

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
from marshmallow import fields

# level5: specify-project packages
# None


class CreatedAtMixin(object):
    created_at = fields.Method("get_created_at")

    def get_created_at(self, obj):
        return obj.id.generation_time.isoformat()
