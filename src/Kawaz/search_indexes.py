# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/03
#
from haystack import indexes

class SearchIndex(indexes.SearchIndex):
    text        = indexes.CharField(document=True, use_template=True)
    created_at  = indexes.DateTimeField(model_attr='created_at')
    updated_at  = indexes.DateTimeField(model_attr='updated_at')