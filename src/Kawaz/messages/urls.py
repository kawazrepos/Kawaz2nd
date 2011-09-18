# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url('^$',                           views.message_index,    name='messages-message-list'),
    url('^recived/$',                   views.message_recived,  name='messages-message-recived'),
    url('^sent/$',                      views.message_sent,     name='messages-message-sent'),
    url('^(?P<object_id>\d+)/$',        views.message_detail,   name='messages-message-detail'),
    url('^create/$',                    views.create_message,   name='messages-message-create'),
    url('^(?P<group>[^/]+)/create/$',   views.create_message,   name='messages-message-create'),
    url('^(?P<object_id>\d+)/delete/$', views.delete_message,   name='messages-message-delete'),
)