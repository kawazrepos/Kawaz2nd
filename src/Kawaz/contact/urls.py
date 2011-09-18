# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',         views.email, name='contact-email'),
)