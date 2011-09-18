# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from ..projects.models import Project
from models import Task

class TaskFilterSet(filterset.FilterSetWithRequest):
    status      = filters.ChoiceFilter(label=u"ステータス", choices=Task.STATUSES, widget=widgets.LinkWidget())
    priority    = filters.ChoiceFilter(label=u"優先度", choices=Task.PRIORITIES, widget=widgets.LinkWidget())
    deadline    = filters.DateRangeFilter(label=u"締切り", widget=widgets.LinkWidget())
    project     = filters.ModelChoiceFilter(label=u"所属プロジェクト", queryset=None, widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Task
        fields = ['status', 'priority', 'deadline', 'tags']
    
    def __init__(self, request=None, *args, **kwargs):
        super(TaskFilterSet, self).__init__(request, *args, **kwargs)
        self.filters['project'].extra['queryset'] = Project.objects.related(request, request.user)