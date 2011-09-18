# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Profile

class ProfileIndex(SearchIndex):
    nickname    = indexes.CharField(model_attr='nickname')
    sex         = indexes.CharField(model_attr='sex', null=True)
    birthday    = indexes.DateField(model_attr='birthday', null=True)
    url         = indexes.CharField(model_attr='url', null=True)
    skills      = indexes.MultiValueField(null=True)
    
    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True).exclude(nickname=None)
    
    def prepare_skills(self, obj):
        return [skill for skill in obj.skills.all()]
site.register(Profile, ProfileIndex)