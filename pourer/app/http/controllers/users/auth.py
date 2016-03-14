#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""auth for Users API
"""
# level1: native python packages
# None

# level2: native web framework packages
from flask import abort
from flask.views import MethodView

# level3: relative web framework plugins
# from flask.ext.login import login_required, current_user

# level4: third-party packages
from webargs.flaskparser import use_args
from mongoengine.errors import NotUniqueError

# level5: specify-project packages
from . import users_bp
from ..mixins import RestfulViewMixin
from ...error_codes import user_errors
from ...requests.users.auth import SignupRequest
from database.user.document import User

# from ...schemas.users import SignupSchema, LoginSchema, ResetPasswordSchema
# from ...error_handlers import user_errors


class SignupView(RestfulViewMixin, MethodView):
    '''SignupView'''

    @use_args(SignupRequest, locations=('json',))
    def post(self, args):
        '''create user'''
        try:
            user = User.create_user(**args)
        except NotUniqueError as err:
            err.data = user_errors.ERR_1001_REGISTERED_ACC
            raise
        return self.get_response(status=201)

'''
class LoginView(RestfulViewMixin, MethodView):

    @use_args(LoginSchema, locations=('json',))
    def post(self, args):
        user = User.authenticate(**args)
        if not user:
            abort(401)
        key = user.login()  # It will return key
        return self.get_response({"key": key}, status=200)


class LogoutView(RestfulViewMixin, MethodView):
    decorators = (login_required,)

    def post(self):
        user = current_user
        user.logout()
        return self.get_response(status=200)
'''

'''
class ResetPasswordView(RestfulViewMixin, MethodView):
    decorators = (login_required,)

    @use_args(ResetPasswordSchema, locations=('json',))
    def put(self, args):
        user = current_user
        if not user.check_password(args['old_password']):
            abort(401)
        user.set_password(args['new_password'])
        user.update()
        return self.get_response(status=200)
'''

# Url patterns: To register views in blueprint
users_bp.add_url_rule('/signup', view_func=SignupView.as_view('signup'))
'''
users_bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
users_bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
users_bp.add_url_rule('/reset_password', view_func=ResetPasswordView.as_view('reset-password'))
'''
