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
from django.contrib.auth.models import AnonymousUser

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
    
    def test_manager_draft(self):
        """events.Event: manager draft works correctly"""
        children = get_children_pgroup()

        foo = User.objects.create_user(username='foo', email='foo@test.com', password='password')
        bar = User.objects.create_user(username='bar', email='bar@test.com', password='password')
        children.add_users((foo, bar))

        foofoo = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=foo,
                updated_by=foo,
                pub_state='public'
            )
        foobar = Event.objects.create(
                title='bar',
                body='bar',
                place='bar',
                period_start=datetime.datetime.now()+datetime.timedelta(days=1),
                period_end=datetime.datetime.now()+datetime.timedelta(days=2),
                author=foo,
                updated_by=foo,
                pub_state='draft'
            )
        barfoo = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=bar,
                updated_by=bar,
                pub_state='draft'
            )
        barbar = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=bar,
                updated_by=bar,
                pub_state='draft'
            )

        mock_request = lambda x: None
        mock_request.user = foo

        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 1)

        mock_request.user = bar
        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 2)

        mock_request.user = AnonymousUser
        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 0)
        
        children.remove_users((foo, bar))
        
        mock_request.user = foo
        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 0)

        mock_request.user = bar
        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 0)

        foo.is_superuser = True
        foo.save()
        mock_request.user = foo
        qs = Event.objects.draft(mock_request)
        self.assertEqual(qs.count(), 3)

        self.events.append(foofoo)
        self.events.append(foobar)
        self.events.append(barfoo)
        self.events.append(barbar)

    def test_manager_active(self):
        """events.Event: manager active works correctly"""
        foo, bar, hoge = self.test_creation()

        admin = User.objects.get(pk=1)
        admin.is_superuser = False
        admin.is_staff = False
        admin.save()

        mock_request = lambda x: None
        mock_request.user = admin

        qs = Event.objects.active(mock_request)
        self.assertEqual(qs.count(), 3)

        foo.period_start = datetime.datetime.now() - datetime.timedelta(days=2)
        foo.period_end = datetime.datetime.now() - datetime.timedelta(days=1)
        foo.save()

        qs = Event.objects.active(mock_request)
        self.assertEqual(qs.count(), 2)

        bar.period_start = None
        bar.period_end = None
        bar.save()

        qs = Event.objects.active(mock_request)
        self.assertEqual(qs.count(), 2)

    def test_attend(self):
        """events.Event: attend works correctly"""
        ufoo = User.objects.create_user(username='foo', email='foo@test.com', password='password')
        ubar = User.objects.create_user(username='bar', email='bar@test.com', password='password')

        foo, bar, hoge = self.test_creation()
        # Note: Author automatically attend the event
        self.assertEqual(foo.attendees.count(), 1)

        foo.attend(ufoo)
        self.assertEqual(foo.attendees.count(), 2)

        foo.attend(ubar)
        self.assertEqual(foo.attendees.count(), 3)
        
        return foo, bar, hoge, ufoo, ubar

    def test_leave(self):
        """events.Event: leave works correctly"""
        foo, bar, hoge, ufoo, ubar = self.test_attend()

        foo.leave(ufoo)
        self.assertEqual(foo.attendees.count(), 2)

        foo.leave(ubar)
        self.assertEqual(foo.attendees.count(), 1)

        # Author cannot leave the event
        admin = User.objects.get(pk=1)
        self.assertRaises(AttributeError, foo.leave, admin)
