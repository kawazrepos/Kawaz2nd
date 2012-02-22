#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of ...


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
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from kawaz.core import get_children_pgroup
from ..models import Event

class BaseTestCase(TestCase):
    """Base TestCase of events views"""
    urls = 'kawaz.apps.events.tests.urls'
    fixtures = ['events_test.yaml']

    def setUp(self):
        # Activate admin
        # Note: Without activating admin, accessing admin profile page may
        #       Fail
        self.foo = User.objects.get(username='foo')
        self.bar = User.objects.get(username='bar')
        self.hoge = User.objects.get(username='hoge')

        if settings.EVENTS_GCAL_SYNC:
            # store original google calender id
            self.gcal_calendar_id_original = settings.EVENTS_GCAL_CALENDAR_ID
            settings.EVENTS_GCAL_CALENDAR_ID = settings.EVENTS_GCAL_CALENDAR_ID_DEBUG

    def tearDown(self):
        # restore original google calender id
        if settings.EVENTS_GCAL_SYNC:
            settings.EVENTS_GCAL_CALENDAR_ID = self.gcal_calendar_id_original

    def login(self, user):
        self.logout()
        assert self.client.login(
                username=user.username, 
                password='password'
            ), 'Login as "%s" failed' % user.username

    def logout(self):
        self.client.logout()

class TestEventListView(BaseTestCase):

    def testAccess(self):
        """events.EventListView: accessing with anonymous user works correctly"""
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, 200)

class TestEventDetailView(BaseTestCase):

    def testAccess(self):
        """events.EventListView: accessing with anonymous user works correctly"""
        # Event1: pub_state = public
        response = self.client.get('/1/')
        self.assertEqual(response.status_code, 200)

        # Event2: pub_state = protected
        response = self.client.get('/2/')
        self.assertEqual(response.status_code, 302)

        self.login(self.bar)
        response = self.client.get('/2/')
        self.assertEqual(response.status_code, 403)

        children = get_children_pgroup()
        children.add_users(self.bar)
        response = self.client.get('/2/')
        self.assertEqual(response.status_code, 200)

        # Event3: pub_state = draft
        self.logout()
        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 302)

        self.login(self.bar)
        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 403)

        self.login(self.foo)
        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 200)
