# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^(?P<ctype_id>\d+)/(?P<object_id>\w+)/$',    views.receive_trackback,    {}, "receive_trackback"),
)
