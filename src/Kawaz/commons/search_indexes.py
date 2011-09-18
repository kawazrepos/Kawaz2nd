# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Material

class MaterialIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    author      = indexes.CharField(model_attr='author')
    license     = indexes.CharField(model_attr='license')
    project     = indexes.CharField(model_attr='project', null=True)
    pv          = indexes.IntegerField(model_attr='pv')
site.register(Material, MaterialIndex)