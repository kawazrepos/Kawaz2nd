# -*- coding: utf-8 -*-
#
# Created:    2010/09/24
# Author:         alisue
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    (r'^$',            views.draft_list,    {}, 'drafts-draft-list'),
)
