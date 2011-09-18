# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from django import template
from django.utils.safestring import mark_safe

from .. import get_default_guest_icon

register = template.Library()

class RenderDefaultGuestIcon(template.Node):
    def __init__(self, request, pattern_name):
        self.request, self.pattern_name = request, pattern_name
        
    def render(self, context):
        request = self.request.resolve(context)
        pattern_name = self.pattern_name.resolve(context)
        seed = request.META['REMOTE_ADDR']
        try:
            seed = int(seed.split('.')[3])
        except:
            seed = 0
        return mark_safe(u"""<img src="%s" />""" % get_default_guest_icon(pattern_name, seed))

@register.tag
def render_default_guest_icon(parser, token):
    u"""
    Syntax:
        {% render_default_guest_icon request as <pattern_name> %}
    """
    bits = token.split_contents()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError("second argument of %r has to be 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        pattern_name = parser.compile_filter(bits[3])
    else:
        raise template.TemplateSyntaxError(u"%s tag require `pattern_name` argument." % bits[0])
    return RenderDefaultGuestIcon(request, pattern_name)