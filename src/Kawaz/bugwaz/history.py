# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/11
#
from django.utils.safestring import mark_safe

from libwaz.contrib.history import site
from libwaz.contrib.history import backends

from models import Report

class ReportHistoryBackend(backends.BasicHistoryBackend):
    def _post_save_callback(self, *args, **kwargs):
        pass
    
    def get_message(self, timeline):
        if timeline.action in ('create', 'update', 'delete'):
            return super(ReportHistoryBackend, self).get_message(timeline)
        
        kwargs = {
            'user': self.get_user(timeline),
            'label': self.get_label(timeline)
        }
        if timeline.action == 'charge':
            return mark_safe(u"「%(label)s」の担当者が決定しました" % kwargs)
        elif timeline.action == 'discharge':
            return mark_safe(u"「%(label)s」の担当者が逃げ出しました" % kwargs)
        elif timeline.action == 'resolved':
            return mark_safe(u"「%(label)s」のバグフィクスが完了しました確認してください" % kwargs)
        elif timeline.action == 'verified':
            return mark_safe(u"「%(label)s」のバグフィクスが確認されました" % kwargs)
        elif timeline.action == 'status':
            return mark_safe(u"「%(label)s」のステータスが更新されました" % kwargs)
site.register(Report, ReportHistoryBackend)