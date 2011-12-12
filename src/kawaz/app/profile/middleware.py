#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Profile application middleware


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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import django.views.static
import django.contrib.auth.views

IGNORE_REDIRECTION_VIEWS = (
    django.views.static.serve,
    django.contrib.auth.views.logout,
)
class ForceRedirectToProfileUpdatePageMiddleware(object):
    """Force redirect to profile update page while user hasn't update profile"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not hasattr(request, 'user'):
            raise RuntimeError(
            """This middleware has to be called after """
            """'django.contrib.auth.middleware.AuthenticationMiddleware'""")
        elif view_func in IGNORE_REDIRECTION_VIEWS:
            return None
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            url = reverse('profiles-profile-update')
            if not profile.nickname and request.path != url:
                return HttpResponseRedirect(url)
        return None
