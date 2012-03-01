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

from views import ProfileListView
from views import ProfileDetailView
from views import ProfileUpdateView

import api.urls

urlpatterns = patterns('',
    url(r'^$', ProfileListView.as_view(), name='profiles-profile-list'),
    url(r'^update/$', ProfileUpdateView.as_view(),
        name='profiles-profile-update'),
    url(r'^(?P<slug>[^/]+)/$', ProfileDetailView.as_view(),
        name='profiles-profile-detail'),
)
