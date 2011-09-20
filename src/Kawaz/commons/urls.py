# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url('^$',                               views.material_filter,                  name='commons-material-list'),
    url('^(?P<object_id>\d+)/$',            views.material_detail,                  name='commons-material-detail'),
    url('^(?P<object_id>\d+)/digest/$',     views.material_digest,                  name='commons-material-digest'),
    url('^(?P<object_id>\d+)/thumbnail/$',  views.material_thumbnail,               name='commons-material-thumbnail'),
    url('^(?P<object_id>\d+)/download/$',   views.material_download,                name='commons-material-download'),
    url('^create/$',                        views.create_material,                  name='commons-material-create'),
    url('^(?P<object_id>\d+)/update/$',     views.update_material,                  name='commons-material-update'),
    url('^(?P<object_id>\d+)/delete/$',     views.delete_material,                  name='commons-material-delete'),
    url('^attache/$',                       views.attache_material,                 name='commons-material-attache'),
    url('^author/(?P<author>[^/]+)/$',              views.material_filter,          name='commons-material-list'),
    url('^project/(?P<project>[^/]+)/$',            views.material_filter,          name='commons-material-list'),
    url('^project/(?P<project>[^/]+)/create/$',     views.create_material,          name='commons-material-create'),
    url('^project/(?P<project>[^/]+)/(?P<author>[^/]+)/$',
        views.material_filter,                  name='commons-material-list'),
    url('^preview/(?P<object_id>\d+)/(?P<filename>.*)$',    views.material_preview,                 name='commons-material-preview'),
)
