# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends.idcalls import IdCallsBackend

from models import Event

class EventCallsBackend(IdCallsBackend):
    def autodiscover(self, instance, **kwargs):
        if instance.pub_state == 'draft':
            return
        super(EventCallsBackend, self).autodiscover(instance, **kwargs)
site.register(Event, EventCallsBackend)