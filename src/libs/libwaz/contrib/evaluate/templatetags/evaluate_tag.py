# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/29
#
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """
    Evaluate template tags in string value
    
    Usage:
        {% evaluate object.textfield %}
        {% evaluate object.textfield based 'base.html' %}
    
    Example:
        `flatpages/default.html`
        ------------------------------------------------
        {% load evaluate_tag %}
        {% evaluate flatpage.content based 'base.html' %}
        ------------------------------------------------
        
        flatpage on database
        ------------------------------------------------
        {% block head %}
        <title>{{ flatpage.title }}</title>
        {% endblock %}
        
        {% block content %}
        <h1>This is a test</h1>
        {% endblock %}
        ------------------------------------------------
    """
    bits = token.split_contents()
    if len(bits) == 2:
        return EvaluateNode(bits[1], based=None)
    elif len(bits) == 4:
        if bits[2] != 'based':
            raise template.TemplateSyntaxError(u"second argument of %s tag must be 'based'" % bits[0])
        return EvaluateNode(bits[1], bits[3])
    raise template.TemplateSyntaxError(u"%s tag required exact two or four tags" % bits[0])

class EvaluateNode(template.Node):
    def __init__(self, variable, based=None):
        self.variable = template.Variable(variable)
        self.based = template.Variable(based) if based else None

    def render(self, context):
        try:
            content = self.variable.resolve(context)
            if self.based:
                based = self.based.resolve(context)
                content = u"""{%% extends "%s" %%}\n%s""" % (based, content)
            t = template.Template(content)
            return t.render(context)
        
        except template.VariableDoesNotExist, template.TemplateSyntaxError:
            return 'Error rendering', self.variable
