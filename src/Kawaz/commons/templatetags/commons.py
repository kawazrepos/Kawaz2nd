# -*- coding: utf-8 -*-
#
# Created:    2010/09/03
# Author:         alisue
#
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from markupfield.fields import Markup
from ..models import Material
import re

register = template.Library()

COMMONS_PATTERN = re.compile(r"\{commons:\W*(?P<object_id>[^}:]+)(?P<size>[\w,]*)\W*\}", re.MULTILINE)

class GetMaterialsFor(template.Node):
    def __init__(self, value_vname, output_vname):
        self.value_vname = value_vname
        self.output_vname = output_vname
    
    def render(self, context):
        value = template.resolve_variable(self.value_vname, context)
        if isinstance(value, Markup):
            value = value.raw
        pk_list = []
        for m in COMMONS_PATTERN.finditer(value):
            pk_list.append(m.group('object_id'))
        context[self.output_vname] = Material.objects.filter(pk__in=pk_list)
        return ''

@register.tag
def get_materials(parser, token):
    u"""
    Syntax:
        {% get_materials for object.body as materials %}
    """
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("Syntax error. a correct syntax is '%s for <text> as <variable>'" % bits[0])
    # TODO: 構文チェック
    return GetMaterialsFor(bits[2], bits[4])

@register.filter
@template.defaultfilters.stringfilter
def parse_commons(value):
    u"""
    Parse the commons tag (like '{commons: pk}')
    
    Syntax::
        {{ <value>|parse_commons }}
    
    """
    def repl(m):
        try:
            material = Material.objects.get(pk=m.group('object_id'))
            preview_html = material.get_thumbnail_display()
            return preview_html
        except Material.DoesNotExist:
            return m.group(0)
    value = re.sub(COMMONS_PATTERN, repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def parse_commons_html(html):
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
            text = parse_commons(textNode)
            textNode.replaceWith(text)
            
        return str(soup)