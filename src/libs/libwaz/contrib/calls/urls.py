# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^clear/$',                                        views.clear_calls,     name='calls-call-clear'),
    url(r'^clear/?notify=(?P<notify>[(true)|(false)])$',    views.clear_calls,     name='calls-call-clear'),
)