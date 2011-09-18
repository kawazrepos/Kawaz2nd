# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Event

class EventIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    author      = indexes.CharField(model_attr='author')
    period_start= indexes.DateTimeField(model_attr='period_start', null=True)
    period_end  = indexes.DateTimeField(model_attr='period_end', null=True)
    place       = indexes.CharField(model_attr='place', null=True)
    members     = indexes.MultiValueField()
    
    def get_queryset(self):
        return Event.objects.exclude(pub_state='draft')
    
    def prepare_members(self, obj):
        return [member for member in obj.members.all()]
site.register(Event, EventIndex)