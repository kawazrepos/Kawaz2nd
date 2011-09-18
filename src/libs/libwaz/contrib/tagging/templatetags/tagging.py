# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType

from ..models import Tag, TaggedItem

register = template.Library()

class RenderTaggingHeadNode(template.Node):
    def render(self, context):
        tags = Tag.objects.all()
        context.push()
        html = render_to_string('tagging/head.html', {'tags': tags}, context)
        context.pop()
        return html
    
class RenderTaggingTagsNode(template.Node):
    def __init__(self, object_vname=None, threshold=None):
        self.object_vname = object_vname
        self.threshold = threshold
        
    def render(self, context):
        object = template.resolve_variable(self.object_vname, context)
        tags  = Tag.objects.get_for_object(object)
        tagged_items = TaggedItem.objects.get_for_object(object)
        ctype = ContentType.objects.get_for_model(object)
        if self.threshold:
            tags = tags[:self.threshold]
            tagged_items = tagged_items[:self.threshold]
        context.push()
        dict_info = {
            'tags':         tags,
            'tagged_items': tagged_items,
            'content_type': ctype.pk,
            'object_id':    object.pk,
            'object':       object,
            'threshold':    self.threshold,
        }
        html = render_to_string('tagging/list_tagged_item.html', dict_info, context)
        context.pop()
        return html

@register.tag
def render_tagging_tags(parser, token):
    u"""Render tag list to ul formatted as tagging editable
    
    Render tag list to ul formatted as tagging editable (which mean
    if you include `django.tagging.js` and configure correctly then
    `edit` feature would be able. to do this, use `render_tagging_head`
    on head section.
    
    Syntax::
        {% render_tagging_tags for <object> %}
        {% render_tagging_tags for <object> of <threshold> %}
    """
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[1] != 'for':
            raise TemplateSyntaxError("second argument of %s tag must be 'for'" % bits[0])
        elif bits[3] != 'of':
            raise TemplateSyntaxError("fourth argument of %s tag must be 'of'" % bits[0])
        return RenderTaggingTagsNode(bits[2], bits[4])
    elif len(bits) == 3:
        if bits[1] != 'for':
            raise TemplateSyntaxError("second argument of %s tag must be 'for'" % bits[0])
        return RenderTaggingTagsNode(bits[2])
    raise TemplateSyntaxError("%s tag takes exactly 3 or 5 arguments." % bits[0])

@register.tag
def render_tagging_head(parser, token):
    u"""Render javascript and css to be able the feature of editing tags
    
    Use this template tag in head block to be able the feature of editing tags.
    
    Syntax:
        {% render_tagging_head %}
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return RenderTaggingHeadNode()
    raise TemplateSyntaxError("%s tag never takes any arguments." % bits[0])