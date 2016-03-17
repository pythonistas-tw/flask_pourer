#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @first_date    20160316
#  @date          20160316
#  @version       0.0
"""Command
"""
# level1: native python packages
from getpass import getpass
import re

# level2: native web framework packages
# None

# level3: relative web framework plugins
from flask.ext.script import Command


# level4: third-party packages
# None

# level5: specify-project packages
from database.user.document import User


class CreateSuperuser(Command):
    """Create superuser"""

    def input_email(self):
        '''input_email'''
        while True:
            email = raw_input("Email address: ")
            if not email:
                print "This field cannot be blank."
                continue

            email_pattern = r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'
            result = re.match(email_pattern, email)
            if not result:
                print "Error: Enter a valid email address."
                continue

            user = User.objects.filter(email=email).first()
            if user:
                print "Error: That email is already taken."
                continue

            return email

    def input_displayname(self, email):
        '''input_displayname'''
        default_displayname = email.split('@')[0]
        displayname = raw_input("Displayname (default is %s): " % default_displayname)
        displayname = displayname if displayname else default_displayname
        return displayname

    def input_password(self):
        '''input_password'''
        while True:
            password = getpass("Password: ")
            password_again = getpass("Password (again): ")
            if not password and not password_again:
                print "Error: Blank passwords aren't allowed."
                continue
            if password != password_again:
                print "Error: Your passwords didn't match."
                continue

            return password

    def run(self):
        '''run'''
        # input process: interact inputting in console
        email = self.input_email()
        displayname = self.input_displayname(email)
        password = self.input_password()

        # model process: create superuser
        User.create_superuser(email=email, displayname=displayname,
                              password=password)
        print "Superuser created successfully."


AUTH_COMMANDS = {
    'createsuperuser': CreateSuperuser(),
}
