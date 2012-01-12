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
from django.conf.urls.defaults import patterns, url, include

from ..views import PermissionGroupListView
from ..views import PermissionGroupDetailView
from ..views import PermissionGroupCreateView
from ..views import PermissionGroupUpdateView
from ..views import PermissionGroupDeleteView

from ..api import urls

urlpatterns = patterns('',
    url(r'^list/$', PermissionGroupListView.as_view(), name='permissiongroups-permissiongroup-list'),
    url(r'^(?P<pk>\d+)/$', PermissionGroupDetailView.as_view(), name='permissiongroups-permissiongroup-detail'),
    url(r'^create/$', PermissionGroupCreateView.as_view(), name='permissiongroups-permissiongroup-create'),
    url(r'^(?P<pk>\d+)/update/$', PermissionGroupUpdateView.as_view(), name='permissiongroups-permissiongroup-update'),
    url(r'^(?P<pk>\d+)/delete/$', PermissionGroupDeleteView.as_view(), name='permissiongroups-permissiongroup-delete'),
    url(r'^', include(urls)),
)
