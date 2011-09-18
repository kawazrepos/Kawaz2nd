# -*- coding: utf-8 -*-
#
# Created:    2010/10/13
# Author:         alisue
#
from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    from re import search
    if search(pattern, request.path):
        return 'active'
    return ''

#
# from snippets: http://djangosnippets.org/snippets/2143/
#
#@register.simple_tag
#def active(menu):
#    return u'active' if menu else u''