#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""querysets

.. _tutorial:
    http://docs.mongoengine.org/guide/querying.html#custom-querysets
"""
# level1: native python packages
from datetime import datetime

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
from mongoengine.queryset import QuerySet
from mongoengine.queryset.visitor import Q

# level5: specify-project packages
# None


class UserQuerySet(QuerySet):
    '''UserQuerySet'''
    def search_user(self, keyword, your_own_email):
        '''search_user'''
        search_lookup = Q(email__icontains=keyword) | Q(displayname__icontains=keyword)
        exclude_lookup = Q(email__ne=your_own_email)
        return self.filter(search_lookup & exclude_lookup)
