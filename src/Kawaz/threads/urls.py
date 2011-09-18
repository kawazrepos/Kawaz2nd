# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                              views.thread_filter, name='threads-thread-list'),
    url(r'^(?P<object_id>\d+)/$',           views.thread_detail, name='threads-thread-detail'),
#    url(r'^(?P<object_id>\d+)/(?P<param>[\d-]+)/$',
#        views.thread_detail, name='threads-thread-detail'),
    url(r'^create/$',                       views.create_thread, name='threads-thread-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_thread, name='threads-thread-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_thread, name='threads-thread-delete'),
    # Project
    url(r'^(?P<project>[^/]+)/$',           views.thread_filter, name='threads-thread-list'),
    url(r'^(?P<project>[^/]+)/create/$',    views.create_thread, name='threads-thread-create'),
)
