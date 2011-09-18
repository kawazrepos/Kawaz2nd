# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/10
#
from django.db.models import Count
from libwaz.contrib.siever import filterset, filters, widgets
from libwaz.contrib.tagging.filters import TaggingFilter

from ..profiles.models import Profile
from models import Component, Version, Report

CHOICE = lambda x: [('', u"全て")]+list(x)

#
# TODO: バグありそう。initialでわたせるか微妙。実験必要
#
class ReportFilterSet(filterset.FilterSetWithRequest):
    component       = filters.ModelChoiceFilter(label=u"コンポーネント", queryset=None, widget=widgets.LinkWidget())
    version         = filters.ModelChoiceFilter(label=u"バージョン", queryset=None, widget=widgets.LinkWidget())
    serverity       = filters.ChoiceFilter(label=u"深刻度", choices=CHOICE(Report.SERVERITIES), widget=widgets.LinkWidget())
    os              = filters.ChoiceFilter(label=u"OS", choices=CHOICE(Report.OPERATING_SYSTEMS), widget=widgets.LinkWidget())
    status          = filters.ChoiceFilter(label=u"進行状況", choices=CHOICE(Report.STATUSES), widget=widgets.LinkWidget())
    resolution      = filters.ChoiceFilter(label=u"処理方法", choices=CHOICE(Report.RESOLUTIONS), widget=widgets.LinkWidget())
    priority        = filters.ChoiceFilter(label=u"優先度", choices=CHOICE(Report.PRIORITIES), widget=widgets.LinkWidget())
    charges         = filters.ModelChoiceFilter(label=u"担当者", queryset=None, widget=widgets.LinkWidget())
    created_at      = filters.DateRangeFilter(label=u'作成日時', widget=widgets.LinkWidget())
    updated_at      = filters.DateRangeFilter(label=u"更新日時", widget=widgets.LinkWidget())
    tags            = TaggingFilter(label=u"タグ", widget=widgets.LinkWidget())
    
    class Meta:
        model = Report
        fields = ('component', 'version', 'serverity', 'os', 'status', 'resolution', 'priority', 'charges', 'created_at', 'updated_at', 'tags')
    
    def __init__(self, request=None, *args, **kwargs):
        if 'product' in kwargs:
            product = kwargs.pop('product')
        else:
            product = None
        super(ReportFilterSet, self).__init__(request, *args, **kwargs)
        qs = Profile.objects.published(request)
        qs = qs.annotate(count=Count('user__reports_charged')).exclude(count__lt=1)
        self.filters['charges'].extra['queryset'] = qs.order_by("-nickname")
        self.filters['component'].extra['queryset'] = Component.objects.filter(product=product)
        self.filters['version'].extra['queryset'] = Version.objects.filter(product=product)