# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *

from views import *

extra_patterns = patterns('',
    # Published Entry
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<object_id>\d+)/$',    entry_detail,        name='blogs-entry-detail'),
    url(r'^today/$',                                                        entry_archive_today,    name='blogs-entry-archive-today'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                    entry_archive_day,      name='blogs-entry-archive-day'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',                                 entry_archive_month,    name='blogs-entry-archive-month'),
    url(r'^(?P<year>\d+)/$',                                                entry_archive_year,     name='blogs-entry-archive-year'),
    url(r'^$',                                                              entry_filter,           name='blogs-entry-list'),
    # Create Update
    url(r'^create/$',                                                       create_entry,           name='blogs-entry-create'),
    url(r'^(?P<object_id>\d+)/update/$',                                    update_entry,           name='blogs-entry-update'),
    url(r'^(?P<object_id>\d+)/delete/$',                                    delete_entry,           name='blogs-entry-delete'),
    url(r'^category/create/$',                                              create_category,        name='blogs-category-create'),
    url(r'^category/(?P<object_id>\d+)/update/$',                           update_category,        name='blogs-category-udpate'),
    url(r'^category/(?P<object_id>\d+)/delete/$',                           delete_category,        name='blogs-category-delete'),
)
urlpatterns = patterns('',
    # Published Entry
    url(r'^today/$',                                                        entry_archive_today,    name='blogs-entry-archive-today'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                    entry_archive_day,      name='blogs-entry-archive-day'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',                                 entry_archive_month,    name='blogs-entry-archive-month'),
    url(r'^(?P<year>\d+)/$',                                                entry_archive_year,     name='blogs-entry-archive-year'),
    url(r'^$',                                                              entry_filter,           name='blogs-entry-list'),
    (r'^(?P<author>\w+)/',                                                  include(extra_patterns)),
)
