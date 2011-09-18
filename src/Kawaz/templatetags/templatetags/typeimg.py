# -*- coding: utf-8 -*-
#
# Created:    2010/09/26
# Author:         alisue
#
from django import template
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from libwaz.contrib.history.models import Timeline
from libwaz.contrib.drafts.models import Draft

register = template.Library()

class RenderContentTypeImageFor(template.Node):
    def __init__(self, object_vname):
        self.object_vname = object_vname
    
    def render(self, context):
        obj = template.resolve_variable(self.object_vname, context)
        if isinstance(obj, (Timeline, Draft)):
            # History Timelineの場合特別に対象オブジェクトのctypeを使用
            ctype = obj.content_type
        elif isinstance(obj, ContentType):
            ctype = obj
        elif isinstance(obj, models.Model):
            ctype = ContentType.objects.get_for_model(obj)
        elif isinstance(obj, basestring):
            ctype = ContentType.objects.get_for_model(models.get_model(*obj.split('.', 1)))
        else:
            raise template.TemplateSyntaxError("<object> must be 'ContentType', 'Model' or 'natural key'.")
        tag = r"""<span class="ctimg %s"></span>""" % "-".join(ctype.natural_key())
        return mark_safe(tag)
@register.tag
def render_ctimg(parser, token):
    """
    Syntax:
        {% render_ctimg for <object> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("second argument of %s tag must be 'for'" % bits[0])
        return RenderContentTypeImageFor(bits[2])
    raise template.TemplateSyntaxError("%s tag has to be written as '%s for <object>'" % (bits[0], bits[0]))

class RenderMimeTypeImageFor(template.Node):
    def __init__(self, mimetype_vname):
        self.mimetype_vname = mimetype_vname
    
    def render(self, context):
        mimetype = template.resolve_variable(self.mimetype_vname, context)
        if mimetype:
            tag = r"""<span class="mtimg %s"></span>""" % " ".join(mimetype.split('/'))
        else:
            tag = r"""<span class="mtimg unknown"></span>"""
        return mark_safe(tag)
@register.tag
def render_mtimg(parser, token):
    """
    Syntax:
        {% render_mtimg for <object> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("second argument of %s tag must be 'for'" % bits[0])
        return RenderMimeTypeImageFor(bits[2])
    raise template.TemplateSyntaxError("%s tag has to be written as '%s for <object>'" % (bits[0], bits[0]))