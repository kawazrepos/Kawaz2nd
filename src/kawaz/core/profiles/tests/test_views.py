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

class BaseTestCase(TestCase):
    """Base TestCase of profile views"""
    urls = 'kawaz.core.profiles.tests.urls'
    fixtures = ['profiles_test.yaml']

    def setUp(self):
        # Activate admin
        # Note: Without activating admin, accessing admin profile page may
        #       Fail
        profile = User.objects.get(pk=1).profile
        profile.nickname = 'foo'
        profile.save()

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
        response = self.client.get('/detail/foo/')
        self.assertEqual(response.status_code, 200)

    def testAccessProtected(self):
        """profile.ProfileDetailView: protected access works correctly"""
        # Anonymous user cannot access (redirect to login page)
        response = self.client.get('/detail/hoge/')
        self.assertEqual(response.status_code, 302)
        # Authenticated user can access
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/detail/hoge/')
        self.assertEqual(response.status_code, 200)



class TestProfileMoodAPIView(BaseTestCase):
    """Test collection for ProfileMoodAPI"""
    def testAccessWithAnonymous(self):
        """profile.API: anonymouse user rejection works correctly"""
        # Logout in case
        self.client.logout()
        response = self.client.get('/api/mood/')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/api/mood/')
        self.assertEqual(response.status_code, 302)
        response = self.client.delete('/api/mood/')
        self.assertEqual(response.status_code, 302)
        response = self.client.put('/api/mood/')
        self.assertEqual(response.status_code, 302)

    def testAccessWithAuthenticated(self):
        """profile.API: updating mood api works correctly"""
        # Login
        assert self.client.login(username='foo', password='password')
        response = self.client.get('/api/mood/')
        self.assertEqual(response.status_code, 405)
        response = self.client.post('/api/mood/')
        self.assertEqual(response.status_code, 405)
        response = self.client.delete('/api/mood/')
        self.assertEqual(response.status_code, 405)

        response = self.client.put('/api/mood/', {'mood': 'barbar'})
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='foo')
        profile = user.profile
        self.assertEqual(profile.mood, 'barbar')

        # Invalid mood message (mood at most 127 characters)
        response = self.client.put('/api/mood/', {'mood': '*' * 128})
        self.assertEqual(response.status_code, 400)
        assert response.content.startswith('Bad Request')
