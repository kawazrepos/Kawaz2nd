# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.utils.safestring import mark_safe

from libwaz.contrib.calls import site
from libwaz.contrib.calls.backends import BasicCallsBackend

from models import Report

class ReportCallsBackend(BasicCallsBackend):
    MESSAGE = u"%(label)s"
    
    def autodiscover(self, instance, created, **kwargs):
        if not created:
            return
        users = instance.product.members().all()
        for user_to in users:
            super(ReportCallsBackend, self).autodiscover(instance, created, user_to=user_to, **kwargs)
    
    def get_message(self, call):
        if not call.content_object:
            return None
        kwargs = {
            'product': call.content_object.product.label,
            'label': self.get_label(call),
        }
        return mark_safe(u"%(product)sに対する新しいバグレポート「%(label)s」があります。確認してください" % kwargs)
site.register(Report, ReportCallsBackend)