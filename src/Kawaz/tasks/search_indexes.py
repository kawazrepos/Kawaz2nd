# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Task

class TaskIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    status      = indexes.CharField(model_attr='status')
    priority    = indexes.CharField(model_attr='priority')
    daedline    = indexes.DateField(model_attr='deadline', null=True)
    project     = indexes.CharField(model_attr='project', null=True)
    author      = indexes.CharField(model_attr='author')
    owners      = indexes.MultiValueField(null=True)
    
    def get_queryset(self):
        return Task.objects.exclude(pub_state='draft')
    
    def prepare_owners(self, obj):
        return [owner for owner in obj.owners.all()]
site.register(Task, TaskIndex)