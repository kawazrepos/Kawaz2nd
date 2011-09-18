# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.contrib.contenttypes.models import ContentType

from sites import site

class DraftManager(object):
    def all(self, request):
        drafts = []
        for model, backend in site._registry.iteritems():
            drafts += backend.autodiscovers(model, request)
        return drafts
    
class Draft(object):
    u"""下書きモデルのラッピングクラス"""
    objects = DraftManager()
    
    def __init__(self, instance, url, label, body, created_at, updated_at):
        self.instance = instance
        self.content_type = ContentType.objects.get_for_model(instance)
        self.url, self.label, self.body = url, label, body
        self.created_at, self.updated_at = created_at, updated_at