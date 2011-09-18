# -*- coding: utf-8 -*-
#
# Created:    2010/10/15
# Author:         alisue
#
from django import template

register = template.Library()

@register.filter
def order_by(value, args=None):
    if isinstance(args, basestring):
        if "," in args:
            args = args.split(",")
            return value.order_by(*args)
        else:
            return value.order_by(args)
    elif not args:
        return value.order_by('?')
    return value.order_by(args)

@register.filter
def filter(value, args):
    u"""
    Syntax:
        {{ queryset|filter:"flag=True" }}
    """
    def parse(value):
        KEYWORDS = {
            'True':     True,
            'False':    False,
            'None':     None,
        }
        if value in KEYWORDS.keys():
            value = KEYWORDS[value]
        elif value.isdigit():
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        return value
    kwargs = {}
    for arg in args.split(","):
        k, v = arg.split('=', 1)
        kwargs[k] = parse(v)
    #
    # なぜだかシランがgiginetのところでエラる。
    # 解決してる時間がないのでとりあえずsettings.DEBUGの
    # 状態で判別してる。本当はこんなのイラン。
    from django.conf import settings
    if not settings.DEBUG:
        return value.filter(**kwargs)
    else:
        return value.all()

@register.filter
def exclude(value, args):
    u"""
    Syntax:
        {{ queryset|exclude:"flag=True" }}
    """
    def parse(value):
        KEYWORDS = {
            'True':     True,
            'False':    False,
            'None':     None,
        }
        if value in KEYWORDS.keys():
            value = KEYWORDS[value]
        elif value.isdigit():
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        return value
    kwargs = {}
    for arg in args.split(","):
        k, v = arg.split('=', 1)
        kwargs[k] = parse(v)
    #
    # なぜだかシランがgiginetのところでエラる。
    # 解決してる時間がないのでとりあえずsettings.DEBUGの
    # 状態で判別してる。本当はこんなのイラン。
    from django.conf import settings
    if not settings.DEBUG:
        return value.exclude(**kwargs)
    else:
        return value.all()