# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                              views.announcement_list,            name='announcements-announcement-list'),
    url(r'^(?P<object_id>\d+)/$',           views.announcement_detail,          name='announcements-announcement-detail'),
    url(r'^archive/(?P<year>\d{4})/$',      views.announcement_archive_year,    name='announcements-announcement-archive-year'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        views.announcement_archive_month,   name='announcements-announcement-archive-month'),
    url(r'^create/$',                       views.create_announcement,          name='announcements-announcement-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_announcement,          name='announcements-announcement-update'),
    url(r'^(?P<object_id>\d+)/dalete/$',    views.delete_announcement,          name='announcements-announcement-delete'),
)