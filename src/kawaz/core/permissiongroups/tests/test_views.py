#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of profile views


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import PermissionGroup

class BaseTestCase(TestCase):
    """Base TestCase of permissiongroups views"""
    urls = 'kawaz.core.permissiongroups.tests.urls'
    fixtures = ['permissiongroups_test.yaml']

    def setUp(self):
        # Activate admin
        # Note: Without activating admin, accessing admin profile page may
        #       Fail
        foo = User.objects.get(username='foo')
        bar = User.objects.get(username='bar')
        hoge = User.objects.get(username='hoge')

        normal_pgroup = PermissionGroup.objects.get(pk=1)
        staff_pgroup = PermissionGroup.objects.get(pk=2)
        promotable_pgroup = PermissionGroup.objects.get(pk=3)

        # Join
        normal_pgroup.add_users(foo)
        staff_pgroup.add_users(bar)
        promotable_pgroup.add_users(hoge)

        # Store
        self.foo = foo
        self.bar = bar
        self.hoge = hoge

    def login(self, user):
        self.logout()
        assert self.client.login(
                username=user.username, 
                password='password'
            ), 'Login as "%s" failed' % user.username

    def logout(self):
        self.client.logout()

class TestPermissionGroupListView(BaseTestCase):

    def testAccessWithAnonymous(self):
        """permissiongroups.PermissionGroupListView: anonymous user rejection works correctly"""
        self.logout()
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)

    def testAccessWithNormalUser(self):
        self.login(self.foo)
        response = self.client.get('/list/')
        #self.assertEqual(response.status_code, 302) # with Django's permission_required
        self.assertEqual(response.status_code, 403)

    def testAccessWithStaffUser(self):
        self.login(self.bar)
        response = self.client.get('/list/')
        #self.assertEqual(response.status_code, 302) # with Django's permission_required
        self.assertEqual(response.status_code, 403)

    def testAccessWithPromotableUser(self):
        self.login(self.hoge)
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 200)
