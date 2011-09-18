# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends.idcalls import IdCallsBackend

from models import Entry

class EntryCallsBackend(IdCallsBackend):
    def autodiscover(self, instance, **kwargs):
        if instance.pub_state == 'draft':
            return
        super(EntryCallsBackend, self).autodiscover(instance, **kwargs)
site.register(Entry, EntryCallsBackend)