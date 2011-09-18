# -*- coding: utf-8 -*-
#
# @author:    giginet
# @date:        2010/10/29
#
from models import Entry

from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

class EntryFilterSet(filterset.FilterSet):
    updated_at  = filters.DateRangeFilter(label=u'最終更新日', widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Entry
        fields = ['updated_at', 'tags']
