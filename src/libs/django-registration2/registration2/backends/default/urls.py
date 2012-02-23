#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
URLconf for requesting, registration and activation, using django-registration-request's
default backend

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

from registration2.views import register
from registration2.views import activate

urlpatterns = patterns('',
    url(r'^activate/complete/$', direct_to_template,
        {'template': 'registration/activation_complete.html'},
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', activate,
        {'backend': 'registration2.backends.default.DefaultBackend'},
        name='registration_activate'),
    url(r'^register/$', register,
        {'backend': 'registration2.backends.default.DefaultBackend'},
        name='registration_register'),
    url(r'^register/complete/$', direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
    url(r'^register/closed/$', direct_to_template,
        {'template': 'registration/registration_closed.html'},
        name='registration_disallowed'),
    url(r'', include('registration.auth_urls')),
)


