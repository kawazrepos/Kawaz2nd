#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
View models of Kawaz events


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
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.utils.text import ugettext_lazy as _

from qwert.http import Http403
from object_permission.decorators import permission_required

from models import Event
from forms import EventForm

class EventListView(ListView):
    def get_queryset(self):
        return Event.objects.published(self.request)

@permission_required('events.view_event')
class EventDetailView(DetailView):
    model = Event

@permission_required('events.add_event')
class EventCreateView(CreateView):
    form_class = EventForm

@permission_required('events.change_event')
class EventUpdateView(UpdateView):
    form_class = EventForm

@permission_required('events.delete_event')
class EventDeleteView(DeleteView):
    form_class = EventForm

@permission_required('events.view_event')
@permission_required('events.attend_event')
class EventAttendView(SingleObjectTemplateResponseMixin, View):
    model = Event
    template_name_suffix = '_attend'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.attend(request.user)
        return redirect(obj)

@permission_required('events.view_event')
@permission_required('events.attend_event')
class EventLeaveView(SingleObjectTemplateResponseMixin, View):
    model = Event
    template_name_suffix = '_leave'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user:
            raise Http403(_('You cannot escape from your event!'))
        return super(EventLeaveView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user:
            raise Http403(_('You cannot escape from your event!'))
        obj.leave(request.user)
        return redirect(obj)

@permission_required('events.view_event')
@permission_required('events.kick_event')
class EventKickView(SingleObjectTemplateResponseMixin, View):
    model = Event
    template_name_suffix = '_kick'
    user_pk = None
    kick = None

    def dispatch(self, request, user_pk, *args, **kwargs):
        self.user_pk = user_pk
        self.kick = User.objects.get(pk=user_pk)
        return super(EventKickView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == self.kick:
            raise Http403(_('You cannot escape from your event!'))
        return super(EventKickView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == self.kick:
            raise Http403(_('You cannot escape from your event!'))
        obj.leave(self.kick)
        return redirect(obj)
