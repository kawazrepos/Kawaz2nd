#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
API urls 


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
from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from kawaz.extensions.piston.authentication import DjangoAuthentication

from handlers import ProfileMoodHandler

auth = DjangoAuthentication()
ad = {'authentication': auth}

profilemood_resource = Resource(handler=ProfileMoodHandler, **ad)

urlpatterns = patterns('',
    url(r'^mood/$', profilemood_resource, name='profiles-api-mood'),
)
