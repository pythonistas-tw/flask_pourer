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
from flask import abort, request
from flask.views import MethodView

# level3: relative web framework plugins
# None

# level4: third-party packages
from webargs.flaskparser import use_args
from mongoengine.errors import NotUniqueError

# level5: specify-project packages
from . import users_bp
from ..mixins import RestfulViewMixin
from ..decorators import token_authentication
from ...error_codes import user_errors
from ...requests.users.auth import (
    SignupRequest, LoginRequest, ResetPasswordRequest
)
from ...schemas.users import UserSchema
from database.user.document import User
from database.token.document import Token


class SignupView(RestfulViewMixin, MethodView):
    '''SignupView'''
    serializer_class = UserSchema

    @use_args(SignupRequest, locations=('json',))
    def post(self, args):
        '''create user'''
        # model process: create user
        try:
            user = User.create_user(**args)
        except NotUniqueError as err:
            err.data = user_errors.ERR_1001_REGISTERED_ACC
            raise

        # response process: serializing object
        serializer = self.serializer_class()
        data = serializer.dump(user).data
        return self.get_response(data, status=201)


class LoginView(RestfulViewMixin, MethodView):
    '''LoginView'''

    @use_args(LoginRequest, locations=('json',))
    def post(self, args):
        '''create token'''
        # model process: create token key
        user = User.login(**args)
        if not user:
            abort(401)
        token = Token(user=user).save()

        # response process: serializing object
        data = {"key": token.key}
        return self.get_response(data, status=200)


class LogoutView(RestfulViewMixin, MethodView):
    '''LogoutView'''
    decorators = (token_authentication,)

    def post(self):
        '''delete token'''
        # model process: get token and delete it
        token = request.authorization
        token.delete()
        return self.get_response(status=200)


class ResetPasswordView(RestfulViewMixin, MethodView):
    '''ResetPasswordView'''
    decorators = (token_authentication,)

    @use_args(ResetPasswordRequest, locations=('json',))
    def put(self, args):
        '''reset password'''
        # model process: get current user
        token = request.authorization
        user = token.user

        # model process: update password
        if not user.check_password(args['old_password']):
            abort(401)
        user.set_password(args['new_password'])
        user.save()

        # model process: delete old token
        Token.objects.delete_old_tokens(
            key=token.key,
            created_at=token.created_at
        )
        return self.get_response(status=200)


# Url patterns: To register views in blueprint
users_bp.add_url_rule('/signup', view_func=SignupView.as_view('signup'))
users_bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
users_bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
users_bp.add_url_rule('/reset_password', view_func=ResetPasswordView.as_view('reset-password'))
