# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/02
#
from haystack import indexes, site

from ..search_indexes import SearchIndex
from models import Announcement

class AnnouncementIndex(SearchIndex):
    title       = indexes.CharField(model_attr='title')
    author      = indexes.CharField(model_attr='author')
    
    def get_queryset(self):
        return Announcement.objects.exclude(pub_state='draft')
site.register(Announcement, AnnouncementIndex)