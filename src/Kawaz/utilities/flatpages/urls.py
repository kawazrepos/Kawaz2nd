# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/09
#
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$',                              views.flatpage_list,        name='flatpages-flatpage-list'),
    url(r'^create/$',                       views.create_flatpage,      name='flatpages-flatpage-create'),
    url(r'^(?P<object_id>\d+)/update/$',    views.update_flatpage,      name='flatpages-flatpage-update'),
    url(r'^(?P<object_id>\d+)/delete/$',    views.delete_flatpage,      name='flatpages-flatpage-delete'),
)