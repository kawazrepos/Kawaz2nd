# -*- coding: utf-8 -*-
#
# get_latest.py
#    Gettin latest list
#
#    Author: Alisue 2010/10/13
#
#
from django import template
from django.db.models import get_model

register = template.Library()

class GetLatestForToAs(template.Node):
    def __init__(self, model, num, output_varname):
        self.model = get_model(*model.split('.', 1))
        self.num = num
        self.output_varname = output_varname
        
    def render(self, context):
        context[self.output_varname] = self.model._default_manager.all()[:self.num]
        return ''
class GetLatestForToByAs(template.Node):
    def __init__(self, model, num, order_by, output_varname):
        self.model = get_model(*model.split('.', 1))
        self.num = num
        self.order_by = order_by.split(',')
        self.output_varname = output_varname
        
    def render(self, context):
        context[self.output_varname] = self.model._default_manager.all().order_by(*self.order_by)[:self.num]
        return ''
    
@register.tag
def get_latest(parser, token):
    u"""
    特定オブジェクトの最新モデルリストを返す
    
    Usage:
        get_latest for <app_label>.<model> to <num> as <variable>
        get_latest for <app_label>.<model> to <num> by "<order_by>,<order_by2>" as <variable>
    """
    bits = token.split_contents()
    
    if len(bits) != 7 and len(bits) != 9:
        raise template.TemplateSyntaxError("%s tag takes exactly four or six arguments" % bits[0])
    elif bits[1] != 'for':
        raise template.TemplateSyntaxError("first argument of %s tag has to be 'for'" % bits[0])
    elif bits[3] != 'to':
        raise template.TemplateSyntaxError("third argument of %s tag has to be 'to'" % bits[0])
    if bits[5] != 'as' and bits[5] != 'by':
        raise template.TemplateSyntaxError("fifth argument of %s tag has be 'as' or 'by'" % bits[0])
    if len(bits) == 9:
        if bits[7] != 'as':
            raise template.TemplateSyntaxError("seventh argument of %s tag has be 'as'" % bits[0])
        return GetLatestForToByAs(bits[2], bits[4], bits[6][1:-1], bits[8])
    else:
        return GetLatestForToAs(bits[2], bits[4], bits[6])