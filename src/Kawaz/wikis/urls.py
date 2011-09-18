# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

#
# Notice:
#    required `(?P<project>[^/]+)`
#
urlpatterns = patterns('',
    url(r'^$',                          views.entry_filter,     name='wikis-entry-list'),
    url(r'index/$',                     views.entry_detail,     name='wikis-entry-detail'),
    url(r'create/$',                    views.create_entry,     name='wikis-entry-create'),
    url(r'(?P<slug>[^/]+)/update/$',    views.update_entry,     name='wikis-entry-update'),
    url(r'(?P<slug>[^/]+)/delete/$',    views.delete_entry,     name='wikis-entry-delete'),
    url(r'(?P<slug>[^/]+)/$',           views.entry_detail,     name='wikis-entry-detail'),
)