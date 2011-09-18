# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/26
#
from django.contrib.auth.models import User

class UserSet(object):
    @classmethod
    def create_user(cls, username, email=None, password=None, is_staff=False, is_superuser=False):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            if not email:
                email = "%s@test.com" % username
            if not password:
                password = username
            user = User.objects.create_user(username, email, password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.get_profile().nickname = username
        user.get_profile().save()
        user.save()
        return user
    def __init__(self):
        self.admin = UserSet.create_user('admin', is_superuser=True)
        self.staff = UserSet.create_user('staff', is_staff=True)
        self.user = UserSet.create_user('user')
        
    def login(self, client, user):
        return client.login(username=user.username, password=user.username)
    def login_admin(self, client):
        return self.login(client, self.admin)
    def login_staff(self, client):
        return self.login(client, self.staff)
    def login_user(self, client):
        return self.login(client, self.user)