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
    author      = indexes.CharField(model_attr='author')
    category    = indexes.CharField(model_attr='category', null=True)
site.register(Entry, EntryIndex)