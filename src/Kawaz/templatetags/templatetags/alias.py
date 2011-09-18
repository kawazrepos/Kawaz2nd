# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from django import template

register = template.Library()

class AliasAs(template.Node):
    def __init__(self, src_vname, dst_vname, force=False):
        self.src_vname = src_vname
        self.dst_vname = dst_vname
    
    def render(self, context):
        try:
            src = template.resolve_variable(self.src_vname, context)
        except template.VariableDoesNotExist:
            return ''
        try:
            src = template.resolve_variable(self.dst_vname, context)
            return ''
        except template.VariableDoesNotExist:
            context[self.dst_vname] = src
            return ''

@register.tag
def alias(parser, token):
    u"""
    Syntax:
        {% alias <src> as <dst> %}
    """
    bits = token.split_contents()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError("thrird arguments of %s tag must be 'as'" % bits[0])
        return AliasAs(bits[1], bits[3])
    raise template.TemplateSyntaxError("Syntax error. the correct syntax is '%s <src> as <dst>' " % bits[0])