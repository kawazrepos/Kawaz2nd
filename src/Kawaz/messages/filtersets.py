# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from ..profiles.models import Profile
from models import Message

class MessageRecivedFilterSet(filterset.FilterSetWithRequest):
    author      = filters.ModelChoiceFilter(label=u'送信者', queryset=None, widget=widgets.LinkWidget())
    created_at  = filters.DateRangeFilter(label=u"送信日", widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Message
        fields = ['author', 'created_at', 'tags']

    def __init__(self, request=None, *args, **kwargs):
        super(MessageRecivedFilterSet, self).__init__(request, *args, **kwargs)
        self.filters['author'].extra['queryset'] = Profile.objects.published(request)
        
class MessageSentFilterSet(filterset.FilterSetWithRequest):
    recivers    = filters.ModelChoiceFilter(label=u'受信者', queryset=None, widget=widgets.LinkWidget())
    created_at  = filters.DateRangeFilter(label=u"送信日", widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Message
        fields = ['recivers', 'created_at', 'tags']

    def __init__(self, request=None, *args, **kwargs):
        super(MessageSentFilterSet, self).__init__(request, *args, **kwargs)
        self.filters['recivers'].extra['queryset'] = Profile.objects.published(request)