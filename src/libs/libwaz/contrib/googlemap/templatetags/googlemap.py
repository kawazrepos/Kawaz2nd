# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/29
#
from django import template
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError

register = template.Library()

class RenderGoogleMapHeadNode(template.Node):
    def render(self, context):
        context.push()
        html = render_to_string('googlemap/head.html', {}, context)
        context.pop()
        return html

@register.tag
def render_googlemap_head(parser, token):
    u"""Render javascript and css to be able the feature of editing tags
    
    Use this template tag in head block to be able the feature of editing tags.
    
    Syntax:
        {% render_googlemap_head %}
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return RenderGoogleMapHeadNode()
    raise TemplateSyntaxError("%s tag never takes any arguments." % bits[0])