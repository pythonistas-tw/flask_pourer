#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
"""request schemas

Field classes for various types of data.
    http://marshmallow.readthedocs.org/en/latest/api_reference.html#module-marshmallow.fields

“Read-only” and “Write-only” Fields
    https://marshmallow.readthedocs.org/en/latest/quickstart.html#read-only-and-write-only-fields

Meta
    http://marshmallow.readthedocs.org/en/latest/api_reference.html#marshmallow.Schema.Meta
"""
from marshmallow import Schema, fields, validate


# Field definations
class CommonFields(object):
    emailfield = fields.Email(required=True, validate=validate.Length(max=255))
    passwordfield = fields.Str(required=True, validate=validate.Length(max=64))
    nicknamefield = fields.Str(validate=validate.Length(max=255))


# Request Schemas
class SignupRequest(Schema):
    email = CommonFields.emailfield
    password = CommonFields.passwordfield
    nickname = CommonFields.nicknamefield

    class Meta:
        strict = True


class ProfileUpdateRequest(Schema):
    displayname = CommonFields.nicknamefield

    class Meta:
        strict = True


class LoginRequest(Schema):
    email = CommonFields.emailfield
    password = CommonFields.passwordfield

    class Meta:
        strict = True


class ResetPasswordRequest(Schema):
    old_password = CommonFields.passwordfield
    new_password = CommonFields.passwordfield

    class Meta:
        strict = True
