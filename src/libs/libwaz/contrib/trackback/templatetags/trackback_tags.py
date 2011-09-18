# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from ..models import Trackback

register = template.Library()

class TrackbackRdfNode(template.Node):
    def __init__(self, obj):
        self.obj_name = obj
        
        
    def render(self, context):
        self.object = template.resolve_variable(self.obj_name, context)
        self.object.ct = ContentType.objects.get_for_model(self.object).pk
        return render_to_string(r'trackback/rdf_include.xml', {'object': self.object, 'SITE_URL': "http://%s" % Site.objects.get_current().domain})

@register.tag
def get_trackback_rdf_for(parser, token):
    u"""
    Usage:
        {% get_trackback_rdf_for <object> %}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "get_trackback_rdf_for tag takes exactly one argument"
    return TrackbackRdfNode(bits[1])

class TrackbacksNode(template.Node):
    def __init__(self, obj, varname):
        self.varname = varname
        self.obj_name = obj
    
    
    def render(self, context):
        self.object = template.resolve_variable(self.obj_name, context)
        context[self.varname] = Trackback.objects.filter(content_type=ContentType.objects.get_for_model(self.object), object_id=self.object.pk).all()
        return ''

@register.tag
def get_trackbacks_for(parser, token):
    u"""
    Usage:
        {% get_trackbacks_for <object> as <variable> %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "get_trackbacks tag takes exactly three arguments"
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "second argument to get_trackbacks tag must be 'as'"
    return TrackbacksNode(bits[1], bits[3])