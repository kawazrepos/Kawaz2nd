#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
API Handler via piston for permissiongroup application


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
from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import throttle

class PromoteHandler(BaseHandler):
    """Promote request.user to superuser"""
    allowed_methods = ('PUT',)

    @throttle(5, 100) # allow 5 times in 100 sec
    def update(self, request):
        user = request.user
        if not user.is_authenticated() or not user.is_promotable:
            return rc.FORBIDDEN
        user.is_superuser = True
        user.save()
        return rc.ALL_OK

class DemoteHandler(BaseHandler):
    """Demote request.user from superuser"""
    allowed_methods = ('PUT',)

    @throttle(5, 100) # allow 5 times in 100 sec
    def update(self, request):
        user = request.user
        if not user.is_authenticated() or not user.is_promotable:
            return rc.FORBIDDEN
        user.is_superuser = False
        user.save()
        return rc.ALL_OK
