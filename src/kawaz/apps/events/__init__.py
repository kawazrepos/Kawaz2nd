#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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
from django.core.exceptions import ImproperlyConfigured

settings.EVENTS_GCAL_SYNC = getattr(settings, 'EVENTS_GCAL_SYNC', False)

if settings.EVENTS_GCAL_SYNC:
    if not hasattr(settings, 'EVENTS_GCAL_LOGIN_NAME'):
        raise ImproperlyConfigured("'EVENTS_GCAL_LOGIN_NAME' is required to sync events with Google Calendar")
    if not hasattr(settings, 'EVENTS_GCAL_LOGIN_PASS'):
        raise ImproperlyConfigured("'EVENTS_GCAL_LOGIN_PASS' is required to sync events with Google Calendar")
    if not hasattr(settings, 'EVENTS_GCAL_CALENDAR_ID'):
        raise ImproperlyConfigured("'EVENTS_GCAL_CALENDAR_ID' is required to sync events with Google Calendar")
    if not hasattr(settings, 'EVENTS_GCAL_CALENDAR_ID_DEBUG'):
        raise ImproperlyConfigured("'EVENTS_GCAL_CALENDAR_ID_DEBUG' is required to sync events with Google Calendar")

