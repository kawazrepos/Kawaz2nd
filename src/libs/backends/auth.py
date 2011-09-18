# -*- coding: utf-8 -*-
#
# Created:    2010/09/27
# Author:         alisue
#
from django.contrib.auth.backends import ModelBackend
from django.contrib.admin.models import User
from django.core.validators import email_re


class EmailAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        #If username is an email address, then try to pull it up
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            #We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
