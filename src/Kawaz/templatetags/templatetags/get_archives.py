# -*- coding: utf-8 -*-
#
# get_archive.py
#    Gettin archive list or adding archive list via Djanog templatetag
#
#    Author: Alisue 2010/11/30
#
#    Ref: http://www.martin-geber.com/thought/2007/10/28/adding-archives-information-django-templatetag/
#
from django import template
from django.db.models import get_model

register = template.Library()

class Archive:
    def __init__(self, date, object_list, count):
        self.date = date
        self.object_list = object_list
        self.count = count

class GetMonthlyArchivesOfForAs(template.Node):
    def __init__(self, model, date_field, author, variable_name):
        self.model = model
        self.date_field= date_field
        self.author = author
        self.variable_name = variable_name
    def render(self, context):
        model = self.model.resolve(context)
        if isinstance(model, basestring):
            model = get_model(*model.split('.', 1))
        date_field = self.date_field.resolve(context)
        qs = model.objects.all()
        if self.author:
            author = self.author.resolve(context)
            qs = qs.filter(author=author)
        date_list = qs.dates(date_field, 'month', order='DESC')
        archives = []
        for date in date_list:
            object_list = qs.filter(**{'%s__year'%date_field: date.year}).filter(**{'%s__month'%date_field: date.month})
            archives.append(Archive(date, object_list, object_list.count()))
        context[self.variable_name] = archives
        return ''

@register.tag
def get_monthly_archives(parser, token):
    u"""
    特定オブジェクトの月間アーカイブを取得する
    
    Usage:
        get_monthly_archive of <model> with <date_field> for <author> as <variable>
        
    """
    bits = token.split_contents()
    if len(bits) == 9:
        if bits[1] != 'of':
            raise template.TemplateSyntaxError("first argument of %r has to be 'of'" % bits[0])
        elif bits[3] != 'with':
            raise template.TemplateSyntaxError("third argument of %r has to be 'with'" % bits[0])
        elif bits[5] != 'for':
            raise template.TemplateSyntaxError("fifth argument of %r has to be 'for'" % bits[0])
        elif bits[7] != 'as':
            raise template.TemplateSyntaxError("seventh argument of %r has to be 'as'" % bits[0])
        model = parser.compile_filter(bits[2])
        date_field = parser.compile_filter(bits[4])
        author = parser.compile_filter(bits[6])
        variable_name = bits[8]
    elif len(bits) == 7:
        if bits[1] != 'of':
            raise template.TemplateSyntaxError("first argument of %r has to be 'of'" % bits[0])
        elif bits[3] != 'with':
            raise template.TemplateSyntaxError("third argument of %r has to be 'with'" % bits[0])
        elif bits[5] != 'as':
            raise template.TemplateSyntaxError("fifth argument of %r has to be 'as'" % bits[0])
        model = parser.compile_filter(bits[2])
        date_field = parser.compile_filter(bits[4])
        author = None
        variable_name = bits[6]
    else:
        raise template.TemplateSyntaxError("%r tag has to be written like 'get_monthly_archives of <model> with <date_field> (for <author>) as <variable>" % bits[0])
    return GetMonthlyArchivesOfForAs(
        model=model,
        date_field=date_field,
        author=author,
        variable_name=variable_name,
    )