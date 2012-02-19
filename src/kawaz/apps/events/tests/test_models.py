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

    def _create_user(self, username):
        kwargs = {
                'username': username,
                'email': '%s@test.com' % username,
                'password': 'password',
            }
        return User.objects.create_user(**kwargs)

    def _create_event(self, title, time, user):
        kwargs = {
                'title': title,
                'body': title.capitalize(),
                'place': title,
                'period_start': time,
                'period_end': time + datetime.timedelta(hours=1),
                'author': user,
                'updated_by': user,
            }
        return Event.objects.create(**kwargs)

    def setUp(self):
        self.foo = self._create_user('foo')
        self.bar = self._create_user('bar')
        self.hoge = self._create_user('hoge')

        if settings.EVENTS_GCAL_SYNC:
            # store original google calender id
            self.gcal_calendar_id_original = settings.EVENTS_GCAL_CALENDAR_ID
            settings.EVENTS_GCAL_CALENDAR_ID = settings.EVENTS_GCAL_CALENDAR_ID_DEBUG

        self.events = []

    def tearDown(self):
        for event in self.events:
            if event.gcal_edit_link:
                event.delete()
        # restore original google calender id
        if settings.EVENTS_GCAL_SYNC:
            settings.EVENTS_GCAL_CALENDAR_ID = self.gcal_calendar_id_original

    def test_creation(self):
        """events.Event: creation works correctly""" 
        now = datetime.datetime.now()
        event1 = self._create_event('event1', now, self.foo)
        event2 = self._create_event('event2', now+datetime.timedelta(days=1), self.foo)
        event3 = self._create_event('event3', now+datetime.timedelta(days=2), self.foo)

        self.assertEquals(event1.title, 'event1')
        self.assertEquals(event1.body.raw, 'Event1')
        self.assertEquals(event1.place, 'event1')
        self.assertEquals(event1.period_start, now)
        self.assertEquals(event1.period_end, now+datetime.timedelta(hours=1))
        self.assertEquals(event1.author, self.foo)
        self.assertEquals(event1.updated_by, self.foo)
        self.assertEquals(event1.attendees.count(), 1)

        # Google Calendar successfully created
        if settings.EVENTS_GCAL_SYNC:
            self.assertNotEquals(event1.gcal_edit_link, None)
            self.assertNotEquals(event2.gcal_edit_link, None)
            self.assertNotEquals(event3.gcal_edit_link, None)

        self.events.append(event1)
        self.events.append(event2)
        self.events.append(event3)

        return event1, event2, event3

    def test_modification(self):
        """events.Event: modification works correctly"""
        event1, event2, event3 = self.test_creation()

        self.assertEquals(event1.title, 'event1')
        event1.title = 'event1mod'
        event1.save()
        self.assertEquals(event1.title, 'event1mod')

    def test_deletion(self):
        """events.Event: deletion works correctly"""
        event1, event2, event3 = self.test_creation()

        event1.delete()
        event2.delete()
        event3.delete()

        # Google Calendar successfully removed
        if settings.EVENTS_GCAL_SYNC:
            self.assertEquals(event1.gcal_edit_link, None)
            self.assertEquals(event2.gcal_edit_link, None)
            self.assertEquals(event3.gcal_edit_link, None)

    def test_manager_published(self):
        """events.Event: manager active works correctly"""
        event1, event2, event3 = self.test_creation()

        event1.pub_state = 'public'
        event1.save()
        event2.pub_state = 'protected'
        event2.save()
        event3.pub_state = 'draft'
        event3.save()
    
        mock_request = lambda x: None
        mock_request.user = self.foo

        qs = Event.objects.published(mock_request)
        self.assertEquals(qs.count(), 1)

        children = get_children_pgroup()
        children.add_users(self.foo)

        qs = Event.objects.published(mock_request)
        self.assertEquals(qs.count(), 2)

        children.remove_users(self.foo)
        self.foo.is_superuser = True
        self.foo.save()
        
        qs = Event.objects.published(mock_request)
        self.assertEquals(qs.count(), 2)
    
    def test_manager_draft(self):
        """events.Event: manager draft works correctly"""
        children = get_children_pgroup()

        children.add_users((self.foo, self.bar))

        foofoo = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=self.foo,
                updated_by=self.foo,
                pub_state='public'
            )
        foobar = Event.objects.create(
                title='bar',
                body='bar',
                place='bar',
                period_start=datetime.datetime.now()+datetime.timedelta(days=1),
                period_end=datetime.datetime.now()+datetime.timedelta(days=2),
                author=self.foo,
                updated_by=self.foo,
                pub_state='draft'
            )
        barfoo = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=self.bar,
                updated_by=self.bar,
                pub_state='draft'
            )
        barbar = Event.objects.create(
                title='foo',
                body='foo',
                place='foo',
                period_start=datetime.datetime.now(),
                period_end=datetime.datetime.now()+datetime.timedelta(hours=1),
                author=self.bar,
                updated_by=self.bar,
                pub_state='draft'
            )

        mock_request = lambda x: None
        mock_request.user = self.foo

        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 1)

        mock_request.user = self.bar
        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 2)

        mock_request.user = AnonymousUser
        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 0)
        
        children.remove_users((self.foo, self.bar))
        
        mock_request.user = self.foo
        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 0)

        mock_request.user = self.bar
        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 0)

        self.foo.is_superuser = True
        self.foo.save()
        mock_request.user = self.foo
        qs = Event.objects.draft(mock_request)
        self.assertEquals(qs.count(), 3)

        self.events.append(foofoo)
        self.events.append(foobar)
        self.events.append(barfoo)
        self.events.append(barbar)

    def test_manager_active(self):
        """events.Event: manager active works correctly"""
        event1, event2, event3 = self.test_creation()

        mock_request = lambda x: None
        mock_request.user = self.foo

        qs = Event.objects.active(mock_request)
        self.assertEquals(qs.count(), 3)

        event1.period_start = datetime.datetime.now() - datetime.timedelta(days=2)
        event1.period_end = datetime.datetime.now() - datetime.timedelta(days=1)
        event1.save()

        qs = Event.objects.active(mock_request)
        self.assertEquals(qs.count(), 2)

        event2.period_start = None
        event2.period_end = None
        event2.save()

        qs = Event.objects.active(mock_request)
        self.assertEquals(qs.count(), 2)

    def test_attend(self):
        """events.Event: attend works correctly"""
        event1, event2, event3 = self.test_creation()

        # Note: Author automatically attend the event
        self.assertEquals(event1.attendees.count(), 1)

        event1.attend(self.bar)
        self.assertEquals(event1.attendees.count(), 2)

        event1.attend(self.hoge)
        self.assertEquals(event1.attendees.count(), 3)
        
        return event1, event2, event3

    def test_leave(self):
        """events.Event: leave works correctly"""
        event1, event2, event3 = self.test_attend()

        event1.leave(self.bar)
        self.assertEquals(event1.attendees.count(), 2)

        event1.leave(self.hoge)
        self.assertEquals(event1.attendees.count(), 1)

        # Author cannot leave the event
        self.assertRaises(AttributeError, event1.leave, self.foo)
