# -*- coding:utf-8 -*-
from django import template
from django.template import TemplateSyntaxError

from ..models import Project

register = template.Library()

class GetProjectsForAs(template.Node):
    def __init__(self, request, status_list, user, variable_name):
        self.request, self.user, self.status_list = request, user, status_list
        self.variable_name = variable_name
        
    def render(self, context):
        request = self.request.resolve(context)
        qs = Project.objects.published(request)
        if self.status_list:
            status_list = [status.resolve(context) for status in self.status_list]
            qs = qs.filter(status__in=status_list)
        if self.user:
            user = self.user.resolve(context)
            qs = qs.filter(members=user)
        context[self.variable_name] = qs
        return ''
@register.tag
def get_projects(parser, token):
    u"""プロジェクトの一覧を表示する
    
    Usage:
        get_projects <request> with <status_list> as <variable>     - Get projects list for <user> and set it to <variable>
        get_projects <request> for <user> as <variable>     - Get projects list for <user> and set it to <variable>
        get_projects <request> as <variable>                - Get project list for all and set it to <variable>
    """
    bits = token.split_contents()
    # get_projects for <user> as <variable>
    if len(bits) == 6:
        if bits[2] != 'for' and bits[2] != 'with':
            raise TemplateSyntaxError("third argument of %s tag must be 'not', 'for' or 'with'" % bits[0])
        elif bits[4] != 'as':
            raise TemplateSyntaxError("fifth argument of %s tag must be 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        if bits[2] == 'with':
            status_list = [parser.compile_filter(v) for v in bits[3].split(',')]
            user = None
        else:
            status_list = None
            user = parser.compile_filter(bits[3])
        variable_name = bits[5]
    # get_projects as <variable>
    elif len(bits) == 4:
        if bits[2] != 'as':
            raise TemplateSyntaxError("third argument of %s tag must be 'for' or 'as'" % bits[0])
        request = parser.compile_filter(bits[1])
        status_list = None
        user = None
        variable_name = bits[3]
    else:
        raise TemplateSyntaxError("%s tag has to be written as 'get_projects <request> (for <user> | with <status_list>) as <variable>'" % bits[0])
    return GetProjectsForAs(request, status_list, user, variable_name)