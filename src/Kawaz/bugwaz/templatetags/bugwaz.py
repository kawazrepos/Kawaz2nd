# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/10
#
from django import template
from ..models import Report

register = template.Library()

class GetStatusReportCountForAs(template.Node):
    def __init__(self, product, variable_name, include, exclude):
        self.product, self.variable_name = product, variable_name
        self.include, self.exclude = include, exclude
        
    def render(self, context):
        product = self.product.resolve(context)
        qs = Report.objects.filter(product=product)
        if self.include:
            qs = qs.filter(status__in=self.include)
        if self.exclude:
            qs = qs.exclude(status__in=self.exclude)
        context[self.variable_name] = qs.count()
        return ''

def get_status_report_count(parser, token, include=None, exclude=None):
    # get_xxxx_report_count for projet as variable
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("first argument of %r has to be 'for'" % bits[0])
        elif bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %r has to be 'as'" % bits[0])
        project = parser.compile_filter(bits[2])
        variable_name = bits[4]
    else:
        raise template.TemplateSyntaxError("%(tag)s has to be written as '%(tag)s for <project> as <variable>'" % {'tag': bits[0]})
    return GetStatusReportCountForAs(project, variable_name, include, exclude)

class GetStatusReportListForAs(template.Node):
    def __init__(self, product, variable_name, include, exclude):
        self.product, self.variable_name = product, variable_name
        self.include, self.exclude = include, exclude
        
    def render(self, context):
        product = self.product.resolve(context)
        qs = Report.objects.filter(product=product)
        if self.include:
            qs = qs.filter(status__in=self.include)
        if self.exclude:
            qs = qs.exclude(status__in=self.exclude)
        context[self.variable_name] = qs
        return ''
def get_status_report_list(parser, token, include=None, exclude=None):
    # get_xxxx_report_list for projet as variable
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("first argument of %r has to be 'for'" % bits[0])
        elif bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %r has to be 'as'" % bits[0])
        project = parser.compile_filter(bits[2])
        variable_name = bits[4]
    else:
        raise template.TemplateSyntaxError("%(tag)s has to be written as '%(tag)s for <project> as <variable>'" % {'tag': bits[0]})
    return GetStatusReportListForAs(project, variable_name, include, exclude)

@register.tag
def get_active_report_count(parser, token):
    u"""
    特定プロジェクトに属するアクティブ(修正完了していない)バグレポート数を取得
    
    Usage:
        get_active_report_count for <project> as <variable>
    """
    return get_status_report_count(parser, token, exclude=['verified'])
@register.tag
def get_active_report_list(parser, token):
    u"""
    特定プロジェクトに属するアクティブ(修正完了していない)バグレポートリストを取得
    
    Usage:
        get_active_report_count for <project> as <variable>
    """
    return get_status_report_list(parser, token, exclude=['verified'])