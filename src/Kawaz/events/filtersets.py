# -*- coding: utf-8 -*-
#
# @author:    giginet
# @date:        2010/10/27
#
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter
from models import Event

from datetime import datetime
from datetime import timedelta

EventDateRangeFilter = filters.DateRangeFilter
EventDateRangeFilter.options = {
        '': (u"いつでも", lambda qs, name: qs.all()),
        1: (u"今日", lambda qs, name: qs.filter(**{
            '%s__year' % name: datetime.today().year,
            '%s__month' % name: datetime.today().month,
            '%s__day' % name: datetime.today().day
        })),
        2: (u"一週間以内", lambda qs, name: qs.filter(**{
            '%s__lte' % name: (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            '%s__gt' % name: (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
        })),
        3: (u"今月", lambda qs, name: qs.filter(**{
            '%s__year' % name: datetime.today().year,
            '%s__month' % name: datetime.today().month
        })),
        4: (u"今年", lambda qs, name: qs.filter(**{
            '%s__year' % name: datetime.today().year,
        })),
    }
class EventFilterSet(filterset.FilterSet):
    period_start    = EventDateRangeFilter(label=u'開催日', widget=widgets.LinkWidget())
    tags            = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Event
        fields = ['period_start', 'tags']

    def __init__(self, *args, **kwargs):
        super(EventFilterSet, self).__init__(*args, **kwargs)