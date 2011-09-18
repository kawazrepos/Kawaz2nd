# -*- coding: utf-8 -*-
#
# @author:    giginet
# @date:        2010/10/29
#
from django.db.models import Count
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from ..profiles.models import Profile
from models import Entry, Category

class EntryFilterSet(filterset.FilterSetWithRequest):
    pub_state       = filters.ChoiceFilter(label=u"公開設定", choices=[('', u"全て")]+list(Entry.PUB_STATES), widget=widgets.LinkWidget())
    category        = filters.ModelChoiceFilter(label=u'カテゴリ', queryset=Category.objects.all(), widget=widgets.LinkWidget())
    publish_at_date = filters.DateRangeFilter(label=u'公開日', widget=widgets.LinkWidget())
    author          = filters.ModelChoiceFilter(label=u"書いた人", queryset=None, widget=widgets.LinkWidget())
    tags            = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Entry
        fields = ['category', 'publish_at_date', 'pub_state', 'author', 'tags']
    
    def __init__(self, request=None, *args, **kwargs):
        super(EntryFilterSet, self).__init__(request, *args, **kwargs)
        qs = Profile.objects.published(request)
        qs = qs.annotate(count=Count('user__blog_entries')).exclude(count__lt=1)
        self.filters['author'].extra['queryset'] = qs.order_by("-nickname")