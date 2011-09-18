# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/27
#
# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.utils.safestring import mark_safe

from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Event

class EventHistoryBackend(backends.BasicHistoryBackend):
    def _post_save_callback(self, *args, **kwargs):
        pass
    
    def get_message(self, timeline):
        if timeline.action in ('join', 'quit'):
            kwargs = {
                'user': self.get_user(timeline),
                'label': self.get_label(timeline)
            }
            if timeline.action == 'join':
                return mark_safe(u"%(user)sさんが「%(label)s」に参加しました" % kwargs)
            elif timeline.action == 'quit':
                return mark_safe(u"%(user)sさんが「%(label)s」への参加をやめました" % kwargs)
        return super(EventHistoryBackend, self).get_message(timeline)
    
    def autodiscover(self, instance, *args, **kwargs):
        if instance.pub_state == 'draft':
            return None
        super(EventHistoryBackend, self).autodiscover(instance, *args, **kwargs)
site.register(Event, EventHistoryBackend)