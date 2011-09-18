# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django import template

from ..models import RegistrationProfile

register = template.Library()

class GetRegistrationUserCountAs(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name
    
    def render(self, context):
        qs = RegistrationProfile.objects.filter(status='waiting')
        context[self.variable_name] = qs.count()
        return ''

@register.tag
def get_registration_user_count(parser, token):
    u"""
    Usage:
        get_registration_user_count as user_count
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if bits[1] != 'as':
            raise template.TemplateSyntaxError("first argument of %r has to be 'as'" % bits[0])
        variable_name = bits[2]
    else:
        raise template.TemplateSyntaxError("%r tag has to be written as 'get_registration_user_count as <variable>'" % bits[0])
    return GetRegistrationUserCountAs(variable_name)