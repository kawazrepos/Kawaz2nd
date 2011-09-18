# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views
import api.urls

urlpatterns = patterns('',
    url('^api/',                            include(api.urls)),
    url('^$',                               views.project_filter,   name='projects-project-list'),
    url('^author/(?P<author>[^/]+)/$',      views.project_filter,   name='projects-project-list'),
    url('^category/(?P<category>[^/]+)/$',  views.project_filter,   name='projects-project-list'),
    url('^create/$',                        views.create_project,   name='projects-project-create'),
    url('^(?P<object_id>\d+)/update/$',     views.update_project,   name='projects-project-update'),
    url('^(?P<object_id>\d+)/delete/$',     views.delete_project,   name='projects-project-delete'),
    url('^(?P<object_id>\d+)/join/$',       views.join_project,     name='projects-project-join'),
    url('^(?P<object_id>\d+)/quit/$',       views.quit_project,     name='projects-project-quit'),
    url('^(?P<object_id>\d+)/quit/(?P<user>[^/]+)/$',
        views.quit_project,     name='projects-project-quit'),
    url('^(?P<slug>[\w_-]+)/$',             views.project_detail,   name='projects-project-detail'),
)