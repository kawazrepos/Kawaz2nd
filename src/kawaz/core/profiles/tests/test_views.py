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
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from kawaz.core import get_children_pgroup

from ..forms import ProfileForm
from ..forms import ServiceFormSet

class BaseTestCase(TestCase):
    """Base TestCase of profile views"""
    fixtures = ['profiles_test.yaml']

    def setUp(self):
        # Activate admin
        # Note: Without activating admin, accessing admin profile page may
        #       Fail
        self.foo = User.objects.get(username='foo')
        self.profile = self.foo.profile
        self.profile.nickname = 'foo'
        self.profile.save()

    def login(self, user):
        self.logout()
        assert self.client.login(
                username=user.username,
                password='password')

    def logout(self):
        self.client.logout()


class TestProfileListView(BaseTestCase):
    """Test collection for ProfileListView"""

    def test_access(self):
        """profile.ProfileListView: access works correctly"""
        response = self.client.get(reverse('profiles-profile-list'))
        self.assertEqual(response.status_code, 200)

class TestProfileDetailView(BaseTestCase):
    """Test collection for ProfileDetailView"""

    def test_access(self):
        """profile.ProfileDetailView: access works correctly"""
        response = self.client.get(reverse('profiles-profile-detail', kwargs={'slug': 'foo'}))
        self.assertEqual(response.status_code, 200)

    def test_access_protected(self):
        """profile.ProfileDetailView: protected access works correctly"""
        # Anonymous user cannot access (redirect to login page)
        url = reverse('profiles-profile-detail', kwargs={'slug': 'hoge'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Authenticated user cannot access either
        self.login(self.foo)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Children can access thus invite foo to children
        children = get_children_pgroup()
        children.add_users(self.foo)
        #self.login(self.foo)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestProfileUpdateView(BaseTestCase):
    def test_access_get(self):
        url = reverse('profiles-profile-update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Authenticated user cannot access either
        self.login(self.foo)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Children can access thus invite foo to children
        children = get_children_pgroup()
        children.add_users(self.foo)
        #self.login(self.foo)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_form.html')
        self.assertTrue(isinstance(response.context['form'], ProfileForm))
        self.assertTrue(isinstance(response.context['formset'], ServiceFormSet))


class TestProfileMoodAPIView(BaseTestCase):
    """Test collection for ProfileMoodAPI"""
    def testAccessWithAnonymous(self):
        """profile.API: anonymouse user rejection works correctly"""
        url = reverse('profiles-api-mood')
        # Logout in case
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 302)

    def testAccessWithAuthenticated(self):
        """profile.API: updating mood api works correctly"""
        # Login
        url = reverse('profiles-api-mood')
        assert self.client.login(username='foo', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

        response = self.client.put(url, {'mood': 'barbar'})
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='foo')
        profile = user.profile
        self.assertEqual(profile.mood, 'barbar')

        # Invalid mood message (mood at most 127 characters)
        response = self.client.put(url, {'mood': '*' * 128})
        self.assertEqual(response.status_code, 400)
        assert response.content.startswith('Bad Request')
