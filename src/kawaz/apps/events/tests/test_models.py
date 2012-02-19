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
import datetime

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from kawaz.core import get_children_pgroup

from ..models import Event

class EventModelTestCase(TestCase):
    """Test collection of event model"""

    def setUp(self):
        self.gcal_calendar_id_original = settings.EVENTS_GCAL_CALENDAR_ID
        settings.EVENTS_GCAL_CALENDAR_ID = settings.EVENTS_GCAL_CALENDAR_ID_DEBUG

        self.events = []

    def tearDown(self):
        settings.EVENTS_GCAL_CALENDAR_ID = self.gcal_calendar_id_original

        for event in self.events:
            if event.gcal_edit_link:
                event.delete()

    def test_creation(self):
        """events.Event: creation works correctly""" 
        admin = User.objects.get(pk=1)
        foo = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=admin,
                updated_by=admin,
            )
        bar = Event.objects.create(
                title='bar',
                body='bar',
                place='bar',
                period_start=datetime.datetime.now()+datetime.timedelta(days=1),
                period_end=datetime.datetime.now()+datetime.timedelta(days=2),
                author=admin,
                updated_by=admin,
            )
        hoge = Event.objects.create(
                title='hoge',
                body='hoge',
                place='hoge',
                period_start=datetime.datetime.now()+datetime.timedelta(days=3),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=2, days=3),
                author=admin,
                updated_by=admin,
            )

        # Google Calendar successfully created
        if settings.EVENTS_GCAL_SYNC:
            assert foo.gcal_edit_link != None
            assert bar.gcal_edit_link != None
            assert hoge.gcal_edit_link != None

        self.events.append(foo)
        self.events.append(bar)
        self.events.append(hoge)

        return foo, bar, hoge

    def test_modification(self):
        """events.Event: modification works correctly"""
        foo, bar, hoge = self.test_creation()

        assert foo.title == 'foo'
        foo.title = 'foofoo'
        foo.save()
        assert foo.title == 'foofoo'

    def test_deletion(self):
        """events.Event: deletion works correctly"""
        foo, bar, hoge = self.test_creation()

        foo.delete()
        bar.delete()
        hoge.delete()

        # Google Calendar successfully removed
        if settings.EVENTS_GCAL_SYNC:
            assert foo.gcal_edit_link == None
            assert bar.gcal_edit_link == None
            assert hoge.gcal_edit_link == None

    def test_manager_published(self):
        """events.Event: manager active works correctly"""
        foo, bar, hoge = self.test_creation()

        foo.pub_state = 'public'
        bar.pub_state = 'protected'
        hoge.pub_state = 'draft'
        foo.save()
        bar.save()
        hoge.save()
    
        admin = User.objects.get(pk=1)
        admin.is_superuser = False
        admin.is_staff = False
        admin.save()

        mock_request = lambda x: None
        mock_request.user = admin

        qs = Event.objects.published(mock_request)
        self.assertEqual(qs.count(), 1)

        children = get_children_pgroup()
        children.add_users(admin)

        qs = Event.objects.published(mock_request)
        self.assertEqual(qs.count(), 2)

        children.remove_users(admin)
        admin.is_superuser = True
        admin.save()
        
        qs = Event.objects.published(mock_request)
        self.assertEqual(qs.count(), 2)



        

