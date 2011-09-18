# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.db.models.fields import CharField, TextField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import force_unicode

from base import BasicCallsBackend

import re

class IdCallsBackend(BasicCallsBackend):
    u"""Calls backend for ID Call (@username)"""
    
    PATTERN = r"@(?P<username>[a-zA-Z0-9_-]+)"
    
    def _get_body_from_instance(self, instance):
        bodies = []
        for field in instance._meta.fields:
            if not isinstance(field, (CharField, TextField)): continue
            bodies.append(force_unicode(getattr(instance, field.name)))
        return "\n".join(bodies)
    
    def _find_users_from_instance(self, instance, pattern=PATTERN):
        body = self._get_body_from_instance(instance)
        users = []
        for username in re.findall(pattern, body):
            try:
                user = User.objects.get(username=username)
                users.append(user)
            except User.DoesNotExist:
                pass
        return users

    def autodiscover(self, instance, created, **kwargs):
        if 'user_to' in kwargs:
            kwargs.pop('user_to')
        user_to_list = self._find_users_from_instance(instance)
        for user_to in user_to_list:
            super(IdCallsBackend, self).autodiscover(instance, created, user_to=user_to, **kwargs)