# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django import template
from ..models import Draft

register = template.Library()

class GetDraftCountAs(template.Node):
    def __init__(self, request, variable_name):
        self.request = request
        self.variable_name = variable_name
    
    def render(self, context):
        request = self.request.resolve(context)
        context[self.variable_name] = len(Draft.objects.all(request))
        return ''

@register.tag
def get_drafts_count(parser, token):
    u"""
    Usage:
        {% get_drafts_count request as drafts_count %}
    """
    bits = token.split_contents()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError(u"second argument of %r has to be 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        variable_name = bits[3]
    else:
        raise template.TemplateSyntaxError(u"%r tag has to be written like {%% get_drafts_count <request> as <variable> %%}" % bits[0])
    return GetDraftCountAs(request=request, variable_name=variable_name)