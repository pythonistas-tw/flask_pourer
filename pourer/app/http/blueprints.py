#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160315
#  @date          20160315
#  @version       0.0
"""blueprints
"""
# level1: native python packages
# None

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
# None

# level5: specify-project packages
from .controllers import users


# Blueprint List: Wrap up the all blueprints
BLUEPRINT_PATTERNS = (
    dict(blueprint=users.users_bp, url_prefix='/users'),
)
