# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from models import Project, Category

class ProjectFilterSet(filterset.FilterSet):
    category    = filters.ModelChoiceFilter(label=u"カテゴリ", queryset=Category.objects.active(), widget=widgets.LinkWidget())
    status      = filters.ChoiceFilter(label=u"ステータス", choices=[('', u"全て")]+list(Project.STATUS), widget=widgets.LinkWidget())
    tags        = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Project
        fields = ['category', 'status', 'tags']