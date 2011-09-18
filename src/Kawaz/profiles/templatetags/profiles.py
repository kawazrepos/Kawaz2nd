# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
# -*- coding: utf-8 -*-
#
# Author:    alisue
# Date:        2010/09/24
#
from django import template
from django.template import TemplateSyntaxError

#from django.contrib.auth.models import User
from ...profiles.models import Profile

register = template.Library()

class GetProfilesAs(template.Node):
    def __init__(self, request, variable_name):
        self.request, self.variable_name = request, variable_name
    
    def render(self, context):
        request = self.request.resolve(context)
        qs = Profile.objects.published(request)
        if request.user.is_authenticated():
            qs.exclude(user__pk=request.user.pk)
        context[self.variable_name] = qs
        return ''

@register.tag
def get_profiles(parser, token):
    u"""
    Usage:
        get_profiles <request> as <variable_name>
    """
    bits = token.split_contents()
    # get_users exclude <user> as <variable>
    if len(bits) == 4:
        if bits[2] != 'as':
            raise TemplateSyntaxError("second argument of %r has to be 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        variable_name = bits[3]
    else:
        raise TemplateSyntaxError("%r tag has to be written as `get_profiles <request> as <variable_name>" % bits[0])
    return GetProfilesAs(request, variable_name)
