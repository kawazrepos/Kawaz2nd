# -*- coding: utf-8 -*-
#
# Created:    2010/09/24
# Author:         alisue
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                              views.profile_filter,   name='profiles-profile-list'),
    url(r'^update/$',                       views.update_profile,   name='profiles-profile-update'),
    url(r'^mood/$',                         views.update_mood_json, name='profiles-profile-update-mood'),
    url(r'^(?P<slug>[^/]+)/$',              views.profile_detail,   name='profiles-profile-detail'),
)
