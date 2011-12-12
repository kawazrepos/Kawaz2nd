#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Kawaz Profile Application

This is Kawaz specified Profile application.
You must include 'kawaz.app.profile' in your ``INSTALLED_APPS`` and
must set ``AUTH_PROFILE_MODULE`` to 'profile.Profile' for using this app.


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

# Check configuration
if not hasattr(settings, 'AUTH_PROFILE_MODULE'):
    raise Exception("""You must set 'AUTH_PROFILE_MODULE' in `settings.py`""")
elif settings.AUTH_PROFILE_MODULE != 'profile.Profile':
    raise Exception("""You must set 'AUTH_PROFILE_MODULE' to """
                    """'profile.Profile' to use Kawaz profile""")
