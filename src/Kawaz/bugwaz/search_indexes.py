# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from models import Product, Report

class ProductIndex(indexes.SearchIndex):
    text        = indexes.CharField(document=True, use_template=True)
    label       = indexes.CharField(model_attr='label')
    group       = indexes.CharField(model_attr='group')
class ReportIndex(indexes.SearchIndex):
    text        = indexes.CharField(document=True, use_template=True)
    product     = indexes.CharField(model_attr='product')
    label       = indexes.CharField(model_attr='label')
    username    = indexes.CharField(model_attr='username')
    component   = indexes.CharField(model_attr='component', null=True)
    version     = indexes.CharField(model_attr='version', null=True)
    os          = indexes.CharField(model_attr='os', null=True)
    status      = indexes.CharField(model_attr='status', null=True)
    resolution  = indexes.CharField(model_attr='resolution', null=True)
    priority    = indexes.CharField(model_attr='priority', null=True)
    charges     = indexes.MultiValueField(null=True)
    created_at  = indexes.DateTimeField(model_attr='created_at')
    updated_at  = indexes.DateTimeField(model_attr='updated_at')
    
    def prepare_charges(self, obj):
        return [user for user in obj.charges.all()]
    
site.register(Product, ProductIndex)
site.register(Report, ReportIndex)