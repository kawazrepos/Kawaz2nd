#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
API Handler via piston for profile application


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
from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import throttle
from piston.utils import rc

from ..models import Event

class EventHandler(BaseHandler):
    """Attend to the event"""
    allowed_method = ('PUT',)
    fields = (
            'pk', 'title', 'body', 'period_start', 'period_end',
            'place', 'address', 'location', 'attendees', 'author'
        )
    model = Event

    @throttle(5, 100) # allow 5 times in 100 sec
    def update(self, request, pk, method, user_pk=None):
        if method == 'kick':
            user = User.objects.get(pk=user_pk)
        else:
            user = request.user
        event = Event.objects.get(pk=pk)
        if method == 'kick' and not user.has_perm('events.kick_event', event):
            return rc.FORBIDDEN
        elif method in ('attend', 'leave') and not user.has_perm('events.attend_event', event):
            return rc.FORBIDDEN
        if method != 'attend' and user == event.author:
            return rc.FORBIDDEN
        method = getattr(event, method)
        method(user)
        return event
