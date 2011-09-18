# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.utils.safestring import mark_safe

from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Thread

class ThreadHistoryBackend(backends.BasicHistoryBackend):
    def _post_save_callback(self, **kwargs):
        pass
    def get_message(self, timeline):
        kwargs = {
            'user':     self.get_user(timeline),
            'label':    self.get_label(timeline),
        }
        if timeline.action == 'create':
            return mark_safe(u"""%(user)sさんが新しく「%(label)s」を立てました""" % kwargs)
        else:
            return super(ThreadHistoryBackend, self).get_message(timeline)
    def autodiscover(self, instance, *args, **kwargs):
        if instance.pub_state == 'draft':
            return None
        return super(ThreadHistoryBackend, self).autodiscover(instance, *args, **kwargs)
    
site.register(Thread, ThreadHistoryBackend)