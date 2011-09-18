# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                             views.permissiongroup_list,      name="permissiongroups-permissiongroup-list"),
    url(r'^(?P<object_id>\d+)/$',          views.permissiongroup_detail,    name="permissiongroups-permissiongroup-detail"),
    url(r'^create/$',                      views.create_permissiongroup,    name="permissiongroups-permissiongroup-create"),
    url(r'^(?P<object_id>\d+)/update/$',   views.update_permissiongroup,    name='permissiongroups-permissiongroup-update'),
    url(r'^(?P<object_id>\d+)/delete/$',   views.delete_permissiongroup,    name='permissiongroups-permissiongroup-delete'),
    url(r'^promote/$',                     views.promote,                   name="permissiongroups-promote"),
    url(r'^demote/$',                      views.demote,                    name="permissiongroups-demote"),
)