# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Project

class ProjectIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    status      = indexes.CharField(model_attr='status')
    category    = indexes.CharField(model_attr='category', null=True)
    author      = indexes.CharField(model_attr='author')
    members     = indexes.MultiValueField(null=True)
    
    def get_queryset(self):
        return Project.objects.exclude(pub_state='draft')
    
    def prepare_members(self, obj):
        return [member for member in obj.members.all()]
site.register(Project, ProjectIndex)