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

from django.utils.html import strip_tags

import logging
logger = logging.getLogger(__name__)

def login(email, password):
    """login to Google Calendar"""
    client = gdata.calendar.service.CalendarService()
    client.email = email
    client.password = password
    try:
        client.ProgrammaticLogin()
        return client
    except gdata.service.CaptchaRequired:
        logger.warn('CaptchaRequired exception has raised. You must unlock the Captcha first.'
                    'See "How do we handle a CAPTCHA challenge?" section of '
                    'http://code.google.com/googleapps/faq.html')
        return None

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
        end_time = when[1]
        end_time = end_time.strftime(timefmt)
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    return event

def insert_event(email, password, calendar_id, event):
    """insert google calendar event into calendar"""
    calendar_url = "/calendar/feeds/%s/private/full" % calendar_id
    client = login(email, password)
    if client:
        event = client.InsertEvent(event, calendar_url)
        return event
    return None

def update_event(email, password, edit_link, event):
    """update google calendar event"""
    client = login(email, password)
    if client:
        event = client.UpdateEvent(edit_link, event)
        return event
    return None

def delete_event(email, password, edit_link):
    """delete google calendar event"""
    client = login(email, password)
    if client:
        client.DeleteEvent(edit_link)
