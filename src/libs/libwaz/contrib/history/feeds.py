# -*- coding: utf-8 -*-
#
# Created:    2010/10/09
# Author:         alisue
#
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
lazy_reverse = lazy(reverse, str)

from models import Timeline

class LatestTimelineFeed(Feed):
    title       = u"最近の更新 - Kawaz.tk"
    description = u"札幌ゲーム製作者コミュニティKawazの全体の更新情報"
    link        = lazy_reverse('history-timeline-feeds')
    
    def items(self):
        queryset = Timeline.objects.order_by('-created_at')
        return queryset[:50]
    
    def item_title(self, item):
        return item.get_message()
    
    def item_description(self, item):
        return item.get_message()
    
    def item_link(self, item):
        return item.get_absolute_url()
