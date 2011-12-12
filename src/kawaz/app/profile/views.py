#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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


def permission_required(perm, model=None):
    """permission required decorator"""
    from django.contrib.auth.views import redirect_to_login
    from qwert.http import Http403
    from object_permission.utils import generic_permission_check
    def wrapper(fn):
        def inner(request, *args, **kwargs):
            queryset = None
            if model:
                queryset = model.objects.all()
            kwargs['slug_field'] = 'user__username'
            if not generic_permission_check(
                    queryset, perm, request, *args, **kwargs):
                if request.user.is_authenticated():
                    raise Http403
                else:
                    return redirect_to_login(request.path)
            return fn(request, *args, **kwargs)
        return inner
    return wrapper


