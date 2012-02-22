#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Urlconf

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
from django.conf.urls.defaults import patterns, url, include

from views import EventListView
from views import EventDetailView
from views import EventCreateView
from views import EventUpdateView
from views import EventDeleteView
from views import EventAttendView
from views import EventLeaveView
from views import EventKickView

import api.urls

urlpatterns = patterns('',
    url(r'^$', EventListView.as_view(), name='events-event-list'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='events-event-detail'),
    url(r'^create/$', EventCreateView.as_view(), name='events-event-create'),
    url(r'^(?P<pk>\d+)/update/$', EventUpdateView.as_view(), name='events-event-update'),
    url(r'^(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='events-event-delete'),
    url(r'^(?P<pk>\d+)/attend/$', EventAttendView.as_view(), name='events-event-attend'),
    url(r'^(?P<pk>\d+)/leave/$', EventLeaveView.as_view(), name='events-event-leave'),
    url(r'^(?P<pk>\d+)/kick/(?P<user_pk>\d+)/$', EventKickView.as_view(), name='events-event-kick'),
    url(r'^', include(api.urls)),
)
