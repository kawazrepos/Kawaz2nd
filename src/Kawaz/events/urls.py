# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                              views.event_filter,         name='events-event-list'),
    url(r'^(?P<object_id>\d+)/$',           views.event_detail,         name='events-event-detail'),
    url(r'^create/$',                       views.create_event,         name='events-event-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_event,         name='events-event-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_event,         name='events-event-delete'),
    url(r'^(?P<object_id>\d+)/join/$',      views.join_event,           name='events-event-join'),
    url(r'^(?P<object_id>\d+)/quit/$',      views.quit_event,           name='events-event-quit'),
    url(r'^(?P<object_id>\d+)/quit/(?P<user>[^/]+)/$',
        views.quit_event,           name='events-event-quit'),
    url(r'^archive/(?P<year>\d+)/$',        views.event_archive_year,   name='events-event-archive-year'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$',
        views.event_archive_month,  name='events-event-archive-month'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.event_archive_day,    name='events-event-archive-day'),
)