# -*- coding: utf-8 -*-
#
# Created:    2010/10/12
# Author:         alisue
#
from django import template

from ..models import Category, Entry

register = template.Library()

class GetCategoriesForAs(template.Node):
    def __init__(self, author, variable_name):
        self.author = author
        self.variable_name = variable_name
    
    def render(self, context):
        author = self.author.resolve(context)
        qs = Category.objects.filter(author=author)
        context[self.variable_name] = qs
        return ''
    
@register.tag
def get_categories(parser, token):
    u"""
    カテゴリーリストを返す
    
    Usage:
        get_categories for <author> as <variable>
    """
    bits = token.split_contents()
    if bits[1] == 'for':
        if bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %s tag must be 'as'" % bits[0])
        author = parser.compile_filter(bits[2])
        variable_name = bits[4]
    else:
        raise template.TemplateSyntaxError("%s tag must be a format like 'get_categories for <author> as <variable>'" % bits[0])
    return GetCategoriesForAs(author, variable_name)

class GetBlogEntriesForAs(template.Node):
    def __init__(self, request, author, variable_name):
        self.request, self.author = request, author
        self.variable_name = variable_name
        
    def render(self, context):
        request = self.request.resolve(context)
        qs = Entry.objects.published(request)
        if self.author:
            author = self.author.resolve(context)
            qs = qs.filter(author=author)
        context[self.variable_name] = qs
        return ''
    
@register.tag
def get_blog_entries(parser, token):
    u"""
    エントリリストを返す
    
    Usage:
        get_entries <request> (for <author>) as <variable>
    """
    bits = token.split_contents()
    if len(bits) == 6:
        if bits[2] != 'for':
            raise template.TemplateSyntaxError("third argument of %s tag must be 'for'"%bits[0])
        elif bits[4] != 'as':
            raise template.TemplateSyntaxError("fifth argument of %s tag must be 'as'"%bits[0])
        request = parser.compile_filter(bits[1])
        author = parser.compile_filter(bits[3])
        variable_name = bits[5]
    elif len(bits) == 4:
        if bits[2] != 'as':
            raise template.TemplateSyntaxError("fifth argument of %s tag must be 'as'"%bits[0])
        request = parser.compile_filter(bits[1])
        author = None
        variable_name = bits[3]
    else:
        raise template.TemplateSyntaxError("%s tag format must be like 'get_entries <request> (for <author>) as <variable>'" % bits[0])
    return GetBlogEntriesForAs(
        request=request,
        author=author,
        variable_name=variable_name
    )