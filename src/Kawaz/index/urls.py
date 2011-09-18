# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    # Admin site
    (r'^$',       views.index, {},     'index'),
)