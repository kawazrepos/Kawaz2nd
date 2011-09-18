# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/15
#
from libwaz.contrib.calls.backends import BasicCallsBackend
from django.utils.translation import ugettext_lazy as _

class CommentCallsBackend(BasicCallsBackend):
    u"""Calls backend for django's comment framework"""
    
    MESSAGE = _('%(user_from)s commented on "%(label)s"')
    
    def autodiscover(self, instance, created, **kwargs):
        content_object = instance.content_object
        if not content_object or not created:
            return
        url = self._get_url_from_instance(content_object)
        user_to = self._get_user_from_instance(content_object)
        label = self._get_label_from_instance(content_object)
        super(CommentCallsBackend, self).autodiscover(instance, created, url=url, user_to=user_to, label=label, **kwargs)