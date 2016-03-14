#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160314
#  @date          20160314
#  @version       0.0
"""Customize token object for mongoengine
"""
# level1: native python packages
import binascii
from datetime import datetime, timedelta
import os

# level2: native web framework packages
# None

# level3: relative web framework plugins
# None

# level4: third-party packages
from mongoengine import Document, fields, CASCADE


# level5: specify-project packages
from ..user.document import User


EXPIRING_TOKEN_LIFESPAN = 60 * 60  # Default: Expired after one hour


class Token(Document):
    # Field classification: basic info fields
    key = fields.StringField(max_length=128, required=True)
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE,
                                 required=True, primary_key=True)

    # Field classification: datetime info field
    created_at = fields.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            {'fields': ['created_at'], 'expireAfterSeconds': EXPIRING_TOKEN_LIFESPAN}
        ]
    }

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(64)).decode()  # It has 128 of length

    def get_lifespan(self):
        difference_datetime = datetime.utcnow() - self.created_at
        rest_lifespan = timedelta(seconds=EXPIRING_TOKEN_LIFESPAN) - difference_datetime
        return str(rest_lifespan)

    def get_expiration_date(self):
        return self.created_at + timedelta(seconds=EXPIRING_TOKEN_LIFESPAN)
