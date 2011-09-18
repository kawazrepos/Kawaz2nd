# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from models import Timeline
from feeds import LatestTimelineFeed

dict_info = {
    'queryset':     Timeline.objects.order_by('-created_at'),
    'paginate_by':  100,
}
urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$',            'object_list',   dict_info,  'history-timeline-list'),
)
urlpatterns += patterns('django.contrib.syndication.views',
    (r'^feeds/$',       LatestTimelineFeed(),   {}, 'history-timeline-feeds'),
)
