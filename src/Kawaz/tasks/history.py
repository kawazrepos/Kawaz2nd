# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.utils.safestring import mark_safe

from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Task
from status import STATUSES_DICT

class TaskHistoryBackend(backends.BasicHistoryBackend):
    def _post_save_callback(self, *args, **kwargs):
        pass
    def get_message(self, timeline):
        kwargs = {
            'user':     self.get_user(timeline),
            'label':    self.get_label(timeline),
        }
        if timeline.action == 'create':
            return mark_safe(u"""%(user)sさんが新しく「%(label)s」を発行しました""" % kwargs)
        elif timeline.action == 'join':
            return mark_safe(u"""%(user)sさんが「%(label)s」の担当者に加わりました""" % kwargs)
        elif timeline.action == 'quit':
            return mark_safe(u"""%(user)sさんが「%(label)s」の担当をキャンセルしました""" % kwargs)
        elif timeline.action in ('update', 'delete'):
            return super(TaskHistoryBackend, self).get_message(timeline)
        else:
            kwargs['status'] = STATUSES_DICT[timeline.action].verbose_name
            return mark_safe(u"""「%(label)s」の状態が%(status)sに変更されました""" % kwargs)
        
    def autodiscover(self, instance, *args, **kwargs):
        if instance.pub_state == 'draft':
            return None
        return super(TaskHistoryBackend, self).autodiscover(instance, *args, **kwargs)
site.register(Task, TaskHistoryBackend)