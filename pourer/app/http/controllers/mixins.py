#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""There is copied from django rest framework's generics.py

https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/generics.py
"""
from flask import json, Response


class RestfulViewMixin(object):
    """Simplify leveraging database"""
    model = None
    serializer_class = None

    def get_object(self, ident):
        """It's copied from Django rest framework.

        .._ link:
            https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/generics.py#L14
            https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/generics.py#L76
        """
        if not self.model:
            raise NotImplementedError("model not set")
        return self.model.query.get_or_404(ident)

    def get_serializer(self):
        """It's copied from Django rest framework.

        .._ link:
            https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/generics.py#L104
        """
        if not self.serializer_class:
            raise NotImplementedError("serializer_class not set")
        serializer_class = self.serializer_class()
        return serializer_class

    @staticmethod
    def get_response(data=None, status=200, headers=None,
                     mimetype=None, content_type="application/json",
                     direct_passthrough=False):
        if data:
            data = json.dumps(data)
        return Response(data, status, headers,
                        mimetype, content_type,
                        direct_passthrough)
