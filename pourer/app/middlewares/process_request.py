#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160316
#  @date          20160316
#  @version       0.0
"""process request middleware
"""
from flask import request, redirect, url_for, abort

from .. import app


@app.before_request
def versioning_api():
    # data process: necessary variables
    version = request.headers.get('HTTP_X_API_VERSION', '')

    # data process: stop request not included HTTP_X_API_VERSION
    if not version:
        abort(403)

    # request process: redirect versioning api if url doesn't include version tag
    path = request.path
    path_list = path.split('/')
    if path_list[1] != version:
        path_list.insert(1, version)
        new_path = '/'.join(path_list)
        print "Redirect versioning api!!"
        return redirect(new_path)
