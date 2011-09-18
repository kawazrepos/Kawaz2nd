# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Entry

class EntryIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    project     = indexes.CharField(model_attr='project')
    author      = indexes.CharField(model_attr='author')
    
    def get_queryset(self):
        return Entry.objects.exclude(pub_state='draft')
site.register(Entry, EntryIndex)