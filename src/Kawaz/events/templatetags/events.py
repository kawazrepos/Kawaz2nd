# -*- coding:utf-8 -*-
from django import template
from django.template import TemplateSyntaxError

from ..models import Event

register = template.Library()

class GetEventsForAs(template.Node):
    def __init__(self, request, user, variable_name, exclude=False):
        self.request, self.user, self.variable_name = request, user, variable_name
        self.exclude = exclude
        
    def render(self, context):
        request = self.request.resolve(context)
        qs = Event.objects.active(request)
        qs = qs.exclude(period_start=None)
        if self.user:
            user = self.user.resolve(context)
            if self.exclude:
                qs = qs.exclude(members=user)
            else:
                qs = qs.filter(members=user)
        context[self.variable_name] = qs
        return ''

@register.tag
def get_events(parser, token):
    u"""開催されているイベントの一覧を表示する
    
    Usage:
        get_events <request> not for <user> as <variable> - Set events which <user> hasn't joined to <variable>
        get_events <request> for <user> as <variable>     - Get events list for <user> and set it to <variable>
        get_events <request> as <variable>                - Get event list for all and set it to <variable>
    """
    bits = token.split_contents()
    if len(bits) == 7:
        if bits[2] != 'not':
            raise TemplateSyntaxError("third argument to get_events tag must be 'not', 'for' or 'as'")
        elif bits[3] != 'for':
            raise TemplateSyntaxError("forth argument to get_events tag after 'not' must be for'")
        elif bits[5] != 'as':
            raise TemplateSyntaxError("sixth argument to get_events tag must be 'as'")
        request = parser.compile_filter(bits[1])
        user = parser.compile_filter(bits[4])
        variable_name = bits[6]
        exclude = True
    # get_events for <user> as <variable>
    elif len(bits) == 6:
        if bits[2] != 'for':
            raise TemplateSyntaxError("third argument to get_events tag must be 'not', 'for' or 'as'")
        elif bits[4] != 'as':
            raise TemplateSyntaxError("fifth argument to get_events tag must be 'as'")
        request = parser.compile_filter(bits[1])
        user = parser.compile_filter(bits[3])
        variable_name = bits[5]
        exclude = False
    # get_events as <variable>
    elif len(bits) == 4:
        if bits[2] != 'as':
            raise TemplateSyntaxError("third argument to get_events tag must be 'for' or 'as'")
        request = parser.compile_filter(bits[1])
        user = None
        variable_name = bits[3]
        exclude = False
    else:
        raise TemplateSyntaxError("get_events tag has to be written as 'get_events <request> not for <user> as <variable>',"
                                  " 'get_events <request> for <user> as <variable>' or 'get_events <request> as <variable>")
    return GetEventsForAs(request, user, variable_name, exclude)
    
