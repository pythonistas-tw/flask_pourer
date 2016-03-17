#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160315
#  @date          20160315
#  @version       0.0
"""querysets

.. _tutorial:
    http://docs.mongoengine.org/guide/querying.html#custom-querysets
"""
# level1: native python packages
# None

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
from mongoengine.queryset import QuerySet

# level5: specify-project packages
# None


class TokenQuerySet(QuerySet):
    '''TokenQuerySet'''

    def delete_old_tokens(self, key, created_at):
        '''delete_old_tokens'''
        old_tokens = self.filter(key=key, created_at__ne=created_at)
        old_tokens.delete()
