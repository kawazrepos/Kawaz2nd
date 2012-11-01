# -*- coding: utf-8 -*-
#
# @date:        2010/10/18
# @author:    alisue
#
u"""
Kawazで使用する以下のフィルターを一度に適用するためのフィルタ
+ viwer.viewer
+ calls.parse_calls
+ commons.parse_commons
"""
from django import template
from django.utils.safestring import mark_safe

import viewer
import urlize_html
from libwaz.contrib.calls.templatetags import calls
from ...commons.templatetags import commons

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def parse(value, full=True):
    if full:
        value = commons.parse_commons(value)
    # URL
    value = urlize_html.urlize_html(value)
    if full:
        # Youtube, NicoNico
        value = viewer.viewer(value)
    # Calls
    value = calls.parse_id_calls_html(value)
    return mark_safe(value)
