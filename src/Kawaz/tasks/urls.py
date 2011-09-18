# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

extra_patterns = patterns('',
    url(r'^$',                              views.task_filter,      name='tasks-task-list'),
    url(r'^create/$',                       views.create_task,      name='tasks-task-create'),
)
urlpatterns = patterns('',
    url(r'^$',                              views.task_filter,      name='tasks-task-list'),
    url(r'^create/$',                       views.create_task,      name='tasks-task-create'),
    url(r'^(?P<object_id>\d+)/$',           views.task_detail,      name='tasks-task-detail'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_task,      name='tasks-task-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_task,      name='tasks-task-delete'),
    url(r'^(?P<object_id>\d+)/status/(?P<status>\w+)/$',
        views.update_task_status,      name='tasks-task-update-status'),
    (r'^(?P<project>[^/]+)/',               include(extra_patterns)),
)