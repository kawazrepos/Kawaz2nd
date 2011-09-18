# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views
import flatpages.urls

urlpatterns = patterns('',
    url(r'^$',                              views.index,                        name='utilities-index'),
    url(r'^resave_all/$',                   views.resave_all,                   name='utilities-resave'),
    url(r'^remodify_object_permission/$',   views.remodify_object_permission,   name='utilities-remodify-object-permission'),
    url(r'^fixture/$',                      views.fixture,                      name='utilities-fixture'),
    url(r'^subversion/$',                   views.subversion,                   name='utilities-subversion'),
    url(r'^email/$',                        views.email,                        name='utilities-email'),
    url(r'^configure/$',                    views.configure,                    name='utilities-configure'),
    url(r'^template_check/(?P<template>.+)/$',  views.template_check,               name='utilities-template-check'),
    (r'^flatpages/',                        include(flatpages.urls)),
)