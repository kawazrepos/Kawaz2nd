# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/27
#
from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Entry

class EntryHistoryBackend(backends.BasicHistoryBackend):
    def autodiscover(self, instance, *args, **kwargs):
        if instance.pub_state == 'draft':
            return None
        elif instance.project.pub_state == 'draft':
            # 下書きのプロジェクトを生成してもタイムラインにwiki作成の通知が出てしまうのを防ぐ
            return None
        return super(EntryHistoryBackend, self).autodiscover(instance, *args, **kwargs)
site.register(Entry, EntryHistoryBackend)