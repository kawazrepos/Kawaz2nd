# -*- coding: utf-8 -*-
#    
#    templatetags.djangostar
#    created by giginet on 2011/09/23
#
from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError

from ..models import Star

register = template.Library()

class RenderDjangoStarHeadNode(template.Node):
    def render(self, context):
        context.push()
        html = render_to_string('star/head.html', {}, context)
        context.pop()
        return html

class RenderDjangoStarListNode(template.Node):
    def __init__(self, object):
        print object
        self.object = template.Variable(object)
        
    def render(self, context):
        object = self.object.resolve(context)
        content_type = ContentType.objects.get_for_model(object)
        context.push()
        html = render_to_string('star/list.html', {
                                                   'content_type' : content_type.pk, 
                                                   'object_id' : object.pk,
                                                   'api_url' : reverse('star-api', args=[content_type.pk, object.pk])
        }, context)
        context.pop()
        return html

@register.tag
def render_djangostar_head(parser, token):
    """Render javascript and css to be able the feature of editing tags
       Use this template tag in head block to be able the feature of editing tags.
       Syntax:
       {% render_djangostar_head %}
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return RenderDjangoStarHeadNode()
    raise TemplateSyntaxError("%s tag don't takes any arguments. " % bits[0])

@register.tag
def render_djangostar_list(parser, token):
    """Render universaltag list as ul list
    Usage:
        {% render_djangostar_list for <object> %}
    """
    bits = token.split_contents()
    if bits[1] != "for":
        raise TemplateSyntaxError("Second argument must be 'for'.")
    if len(bits) == 3:
        return RenderDjangoStarListNode(bits[2])
    raise TemplateSyntaxError("%s tag takes exactly 3 arguments." % bits[0])