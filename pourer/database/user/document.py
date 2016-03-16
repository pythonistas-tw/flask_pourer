#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160311
#  @date          20160311
#  @version       0.0
"""Customize User object for mongoengine

.. _It's copied form:
    https://github.com/MongoEngine/mongoengine/blob/0.9/mongoengine/django/auth.py#L202
"""
# level1: native python packages
from datetime import datetime

# level2: native web framework packages
# None

# level3: relative web framework plugins
from werkzeug.security import generate_password_hash, check_password_hash

# level4: third-party packages
from mongoengine import fields, Document

# level5: specify-project packages
from .queryset import UserQuerySet


class User(Document):
    """A User document that aims to mirror most of the API specified by Django
    at http://docs.djangoproject.com/en/dev/topics/auth/#users
    """
    # Field classification: basic info fields
    email = fields.EmailField(unique=True)
    password = fields.StringField(max_length=128)
    displayname = fields.StringField(max_length=30)

    # Field classification: permission info fields
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)

    # Field classification: datetime info fields
    last_login = fields.DateTimeField()
    date_joined = fields.DateTimeField(default=datetime.utcnow)

    # meta
    meta = {
        'allow_inheritance': True,
        'queryset_class': UserQuerySet,
    }

    def __unicode__(self):
        return "<User(email='%s')>" % (self.email)

    def is_admin(self):
        """is_admin"""
        return self.is_active and self.is_superuser and self.is_staff

    def set_password(self, raw_password):
        """instancemethod - set_password
        """
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """instancemethod - check_password
        """
        return check_password_hash(self.password, raw_password)

    @classmethod
    def create_user(cls, email, password, displayname=None):
        """classmethod - create_user
        """
        if not displayname:
            displayname, _ = email.strip().split('@', 1)

        user = cls(displayname=displayname, email=email)
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def create_superuser(cls, email, password, displayname=None):
        """classmethod - create_superuser
        """
        if not displayname:
            displayname, _ = email.strip().split('@', 1)

        user = cls(
            displayname=displayname,
            email=email,
            is_active=1,
            is_superuser=1,
            is_staff=1
        )
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def login(cls, email, password):
        """classmethod - login"""
        now = datetime.utcnow()
        user = cls.objects.filter(email=email).first()

        # Validation process: Using Short-circuit evaluation to check invalid user
        if not user or not user.check_password(password):
            return None

        user.last_login = now
        user.save()
        return user
