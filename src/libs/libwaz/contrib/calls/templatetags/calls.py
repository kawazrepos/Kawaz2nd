# -*- coding: utf-8 -*-
#
# Created:    2010/10/10
# Author:         alisue
#
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from ..models import Call
from ..backends import IdCallsBackend

import re

register = template.Library()

class GetCallsForAs(template.Node):
    def __init__(self, user, variable_name):
        self.user, self.variable_name = user, variable_name
        
    def render(self, context):
        user = self.user.resolve(context)
        if user.is_authenticated():
            qs = Call.objects.exclude(read=True).filter(user_to=user)
            context[self.variable_name] = qs
        return u''
    
@register.tag
def get_calls(parser, token):
    u"""
    Return calls for particular user
    
    Usage:
        get_calls for <user> as <variable>
    """
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("first argument of %r tag must be 'for'" % bits[0])
        elif bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %r tag must be 'as'" % bits[0])
        user = parser.compile_filter(bits[2])
        variable_name = bits[4]
        return GetCallsForAs(user, variable_name)
    raise template.TemplateSyntaxError("%r tag must be a format like 'get_calls for <user> as <variable>'" % bits[0])

@register.filter
@template.defaultfilters.stringfilter
def parse_id_calls(value):
    u"""
    Parse id call (@username) to <a> link
    """
    def repl(m):
        username = m.group('username')
        try:
            user = User.objects.get(username=username)
            url = user.get_absolute_url()
            return """<a href="%(url)s">%(value)s</a>""" % {
                'url': url,
                'value': m.group(0)
            }
        except User.DoesNotExist:
            return m.group(0)
    value = re.sub(IdCallsBackend.PATTERN, repl, unicode(value))
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def parse_id_calls_html(html):
    """
    Returns urls found in an (X)HTML text node element as urls via Django urlize filter.
    """
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in urlize_html The Python BeautifulSoup libraries aren't installed."
        return html
    else:
        soup = BeautifulSoup(html)
           
        textNodes = soup.findAll(text=True)
        for textNode in textNodes:
            text = parse_id_calls(textNode)
            textNode.replaceWith(text)
            
        return str(soup)