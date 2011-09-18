# -*- coding:utf-8 -*-
from django import template
from django.template import TemplateSyntaxError

from ..models import Announcement

register = template.Library()

class GetAnnouncementsAs(template.Node):
    def __init__(self, request, variable_name):
        self.request, self.variable_name = request, variable_name

    def render(self, context):
        request = self.request.resolve(context)
        context[self.variable_name] = Announcement.objects.published(request).exclude(sage=True)
        return ''

@register.tag
def get_announcements(parser, token):
    u"""お知らせの一覧を表示
    
    Usage:
        get_announcements <request> as <variable>    - Get announcement list for all and set it to <variable>
    
    """
    bits = token.split_contents()
    if len(bits) == 4:
        if bits[2] != 'as':
            raise TemplateSyntaxError("second argument to get_annonuncements tag must be 'for' or 'as'")
        request = parser.compile_filter(bits[1])
        variable_name = bits[3]
        return GetAnnouncementsAs(request, variable_name)
    raise TemplateSyntaxError("get_announcements tag has to be written as 'get_announcements <request> as <variable>")
