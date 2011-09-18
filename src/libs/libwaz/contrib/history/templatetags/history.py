# -*- coding: utf-8 -*-
#
# Created:    2010/09/26
# Author:         alisue
#
from django import template
from django.db.models import Manager, Model
from django.db.models.query import QuerySet

from ..models import Timeline

register = template.Library()

class GetHistoryTimelinesForAs(template.Node):
    def __init__(self, object_list, user, variable_name):
        self.object_list, self.user = object_list, user
        self.variable_name = variable_name
    
    def render(self, context):
        if self.user:
            user = self.user.resolve(context)
            qs = Timeline.objects.filter(user=user)
        else:
            qs = Timeline.objects.all()
        if self.object_list:
            urls = []
            for object in self.object_list:
                object = object.resolve(context)
                if isinstance(object, (QuerySet, Manager)):
                    for x in object.all(): urls.append(x.get_absolute_url())
                elif isinstance(object, Model):
                    urls.append(object.get_absolute_url())
                else:
                    raise AttributeError("<object_list> has to be a instances one of [QuerySet, Manager, Model].")
            qs = Timeline.objects.filter(url__in=urls)
        qs = qs.order_by('-created_at')
        context[self.variable_name] = qs
        return ''

@register.tag
def get_history_timelines(parser, token):
    u"""
    Get history timelines
    
    Usage:
        {% get_history_timelines of <object_lists> for <user> as <variable> %}
        {% get_history_timelines of <object_lists> as <variable> %}
        {% get_history_timelines for <user> as <variable> %}
        {% get_history_timelines as <variable> %}
    object_list:
        <object_list> must be `QuerySet`, `Managr` or `Model` instance.
    
    Example:
        get_history_timelines request for user,user.blog_entries,user.get_profile as timeline
    """
    bits = token.split_contents()
    if len(bits) == 7:
        if bits[1] != 'of':
            raise template.TemplateSyntaxError("first argument of %r tag must be 'of'" % bits[0])
        elif bits[3] != 'for':
            raise template.TemplateSyntaxError("third argument of %r tag must be 'for'" % bits[0])
        elif bits[5] != 'as':
            raise template.TemplateSyntaxError("fifth argument of %r tag must be 'as'" % bits[0])
        object_list = [parser.compile_filter(o) for o in bits[2].split(',')]
        user = parser.compile_filter(bits[4])
        variable_name = bits[6]
    elif len(bits) == 5:
        if bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %r tag must be 'as'" % bits[0])
        elif bits[1] == 'of':
            object_list = [parser.compile_filter(o) for o in bits[2].split(',')]
            user = None
            variable_name = bits[4]
        elif bits[1] == 'for':
            object_list = None
            user = parser.compile_filter(bits[2])
            variable_name = bits[4]
        else:
            raise template.TemplateSyntaxError("first argument of %r tag must be 'of' or 'for'" % bits[0])
    elif len(bits) == 3:
        if bits[1] != 'as':
            raise template.TemplateSyntaxError("first argument of %r tag must be 'as'" % bits[0])
        object_list = None
        user = None
        variable_name = bits[2]
    else:
        raise template.TemplateSyntaxError("%(tag)r tag must be written as '%(tag)r (of <object_list>) (for <user>) as <variable>'" % {'tag': bits[0]})
    return GetHistoryTimelinesForAs(object_list, user, variable_name)

from libwaz.utils.humanize import humanize_datetime
@register.filter
def humanize_date(value):
    return humanize_datetime(value, weekday=False, time=True)
