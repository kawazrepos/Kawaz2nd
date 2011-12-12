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
from ..models import Profile

class BaseTestCase(TestCase):
    """Base TestCase of profile views"""
    urls = 'kawaz.app.profile.tests.urls'
    fixtures = ['test.yaml']

class TestProfileFilterView(BaseTestCase):
    """Test collection for ProfileFilterView"""

    def testAccess(self):
        """profile.ProfileFilterView: access works correctly"""
        response = self.client.get('/filter/')
        self.assertEqual(response.status_code, 200)

class TestProfileListView(BaseTestCase):
    """Test collection for ProfileListView"""

    def testAccess(self):
        """profile.ProfileListView: access works correctly"""
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 200)

class TestProfileDetailView(BaseTestCase):
    """Test collection for ProfileDetailView"""

    def testAccess(self):
        """profile.ProfileDetailView: access works correctly"""
        response = self.client.get('/detail/admin/')
        self.assertEqual(response.status_code, 200)

    def testAccessProtected(self):
        """profile.ProfileDetailView: protected access works correctly"""
        # Anonymous user cannot access (redirect to login page)
        response = self.client.get('/detail/hogehoge/')
        self.assertEqual(response.status_code, 302)
        # Authenticated user can access
        self.client.login(username='foobar', password='password')
        response = self.client.get('/detail/hogehoge/')
        self.assertEqual(response.status_code, 200)

