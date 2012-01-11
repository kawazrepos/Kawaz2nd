#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of profile application middleware


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

class TestForceRedirectToProfileUpdatePageMiddleware(TestCase):
    """Test collection for ProfileFilterView"""
    urls = 'kawaz.core.profile.tests.urls'

    def setUp(self):
        # Activate admin
        # Note: Without activating admin, accessing admin profile page may
        #       Fail
        profile = User.objects.get(pk=1).get_profile()
        profile.nickname = 'admin'
        profile.save()
        # Create inactive user
        self.user = User.objects.create_user(
            username='hogehogefoofoo',
            email='hogehogefoofoo@test.com',
            password='password')
    def tearDown(self):
        self.user.delete()

    def testAccess(self):
        """profile.ForceRedirectToProfileUpdatePageMiddleware: redirection works correctly"""
        # redirection works while user.profile.nickname is None
        self.client.login(username='hogehogefoofoo', password='password')
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/detail/admin/')
        self.assertEqual(response.status_code, 302)
        # set user.profile.nickname
        #profile = self.user.get_profile()
        profile = self.user.profile
        profile.nickname = 'hogehogefoofoo'
        profile.save()
        # nomore redirection
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/detail/admin/')
        self.assertEqual(response.status_code, 200)
