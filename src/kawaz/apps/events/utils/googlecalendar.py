#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Google Calendar Utility (Google API v1.0)


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
import atom
import gdata.service
import gdata.calendar.service

from django.conf import settings
from django.utils.html import strip_tags

settings.GCAL_CALENDAR_ID = getattr(settings, 'GCAL_CALENDAR_ID', None)
settings.GCAL_LOGIN_EMAIL = getattr(settings, 'GCAL_LOGIN_EMAIL', None)
settings.GCAL_LOGIN_PASS = getattr(settings, 'GCAL_LOGIN_PASS', None)

def login(email=None, password=None):
    """login to Google Calendar"""
    client = gdata.calendar.service.CalendarService()
    client.email = email or settings.GCAL_LOGIN_EMAIL
    client.password = password or settings.GCAL_LOGIN_PASS
    try:
        client.ProgrammaticLogin()
        return client
    except gdata.service.BadAuthentication, e:
        if not settings.GCAL_LOGIN_EMAIL and not settings.GCAL_LOGIN_PASS:
            # Ok, Synking with Google Calendar is not required
            return None
        else:
            raise e

def create_event(title, content, where, when):
    """create a google calendar event instance"""
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=strip_tags(content))
    if where:
        event.where.append(gdata.calendar.Where(value_string=where))
    if when:
        # ToDo: timezone should be assumed.
        timefmt = '%Y-%m-%dT%H:%M:%S.000+09:00'
        start_time = when[0]
        start_time = start_time.strftime(timefmt)
        print 'start_time', start_time
        end_time = when[1]
        end_time = end_time.strftime(timefmt)
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    return event

def insert_event(event, calendar_id=None):
    """insert google calendar event into calendar"""
    calendar_id = calendar_id or settings.GCAL_CALENDAR_ID
    calendar_url = "/calendar/feeds/%s/private/full" % calendar_id
    client = login()
    if client:
        event = client.InsertEvent(event, calendar_url)
        return event
    return None

def update_event(edit_link, event):
    """update google calendar event"""
    client = login()
    if client:
        event = client.UpdateEvent(edit_link, event)
        return event
    return None

def delete_event(edit_link):
    """delete google calendar event"""
    client = login()
    if client:
        client.DeleteEvent(edit_link)
