#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Test collection of profile application models


.. Note::
    Adding 'django.contrib.comments' to ``INSTALLED_APPS`` is required to
    execute this test collection. I don't know why but removing user may fail
    without the application.

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
from django.conf import settings

# check required application is in INSTALLED_APPS
if 'django.contrib.comments' not in settings.INSTALLED_APPS:
    raise Exception(
            """'django.contrib.comments' is required in INSTALLED_APPS to """
            """execute this test collection.""")

