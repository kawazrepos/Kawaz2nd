# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
# Ref: http://djangosnippets.org/snippets/1572/
#    : http://djangosnippets.org/snippets/1350/
#
"""
A smarter {% if %} tag for django templates.

While retaining current Django functionality, it also handles equality,
greater than and less than operators. Some common case examples::

    {% if articles|length >= 5 %}...{% endif %}
    {% if "ifnotequal tag" != "beautiful" %}...{% endif %}
"""
import unittest
from django import template
from django.template.defaulttags import TemplateIfParser, IfNode

register = template.Library()

@register.tag('if')
def smart_if(parser, token):
    if_elifs = []
    if_spelling = 'if'
    
    class Enders(list):
        def __contains__(self, val):
            return val.startswith('elif') or val in ['else', 'endif']
    enders = Enders()
                
    while True:
        contents = token.split_contents()
        command = contents[0]
        bits = contents[1:]
        if command == if_spelling:
            var = TemplateIfParser(parser, bits).parse()
            nodelist = parser.parse(enders)
            next_token = parser.next_token()
            if_elifs.append((var, nodelist, token))
            if_spelling = 'elif'
            token = next_token
        elif token.contents == 'else':
            nodelist_false = parser.parse(('endif',))
            parser.delete_first_token()
            break
        elif token.contents == 'endif':
            nodelist_false = template.NodeList()
            break
    while len(if_elifs) > 1:
        var, nodelist_true, token = if_elifs.pop()
        false_node = IfNode(var, nodelist_true, nodelist_false)
        nodelist_false = parser.create_nodelist()
        parser.extend_nodelist(nodelist_false, false_node, token)
    var, nodelist_true, token = if_elifs[0]
    return IfNode(var, nodelist_true, nodelist_false)

if __name__ == '__main__':
    unittest.main()