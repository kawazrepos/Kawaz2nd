# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Thread

class ThreadIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    project     = indexes.CharField(model_attr='project', null=True)
    author      = indexes.CharField(model_attr='author')
    response    = indexes.MultiValueField()
    
    def get_queryset(self):
        return Thread.objects.exclude(pub_state='draft')
    
    def prepare_respnse(self, obj):
        return [r for r in obj.response.all()]
site.register(Thread, ThreadIndex)