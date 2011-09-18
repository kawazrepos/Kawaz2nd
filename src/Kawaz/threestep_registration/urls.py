# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/08
#
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import activate, register
from views import list, withdraw, csv_registration
from backends import ThreeStepBackend

urlpatterns = patterns('',
    url(r'^activate/complete/$', direct_to_template,
        { 'template': 'registration/activation_complete.html' },
        name='registration_activation_complete'),
    url(r'^withdraw/$',
       withdraw,
       name='registration_withdraw'),
    url(r'^list/$',
       list,
       { 'backend': ThreeStepBackend },
       name='registration_list'),
    url(r'^csv_registration/$',
       csv_registration,
       { 'backend': ThreeStepBackend },
       name='registration_csv_registration'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        { 'backend': ThreeStepBackend },
        name='registration_activate'),
    url(r'^register/$',
        register,
        { 'backend': ThreeStepBackend },
        name='registration_register'),
    url(r'^register/complete/$',
        direct_to_template,
        { 'template': 'registration/registration_complete.html' },
        name='registration_complete'),
    url(r'^register/closed/$',
        direct_to_template,
        { 'template': 'registration/registration_closed.html' },
        name='registration_disallowed'),
    (r'', include('registration.auth_urls')),
)
