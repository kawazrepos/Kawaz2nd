# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/29
#
from django import template

register = template.Library()

class GetUnreadCount(template.Node):
    def __init__(self, user, variable_name):
        self.user, self.variable_name = user, variable_name
    def render(self, context):
        user = self.user.resolve(context)
        qs = user.recived_messages.filter(states__read=False)
        context[self.variable_name] = qs.count()
        return ''
@register.tag
def get_unread_message_count(parser, token):
    u"""
    Usage:
        get_unread_message_count for user as variable
    """
    bits = token.split_contents()
    if len(bits) == 5:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("first argument of %r has to be 'for'" % bits[0])
        elif bits[3] != 'as':
            raise template.TemplateSyntaxError("third argument of %r has to be 'as'" % bits[0])
        user = parser.compile_filter(bits[2])
        variable_name = bits[4]
    else:
        raise template.TemplateSyntaxError("%r has to be written as 'get_unread_message_count for <user> as <variable>'" % bits[0])
    return GetUnreadCount(user, variable_name)

class IfHasReadNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, message, user, nodelist_true, nodelist_false, negate):
        self.message, self.user = message, user
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfHasReadNode>"

    def render(self, context):
        message = self.message.resolve(context, True)
        user = self.user.resolve(context, True)
        result = message.states.get(user=user).read
        if (self.negate and not result) or (not self.negate and result):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_ifhasread(parser, token, negate):
    tagname = token.split_contents()[0]
    
    if_elifs = []
    if_spelling = tagname
    endif_spelling = 'end' + tagname
    
    def parse(bits):
        if len(bits) != 3:
            raise template.TemplateSyntaxError("%r takes three arguments" % tagname)
        elif bits[1] != 'for':
            raise template.TemplateSyntaxError("second argument of %r must be `for`" % tagname)
        message = parser.compile_filter(bits[0])
        user = parser.compile_filter(bits[2])
        return message, user
    
    class Enders(list):
        def __contains__(self, val):
            return val.startswith('elif') or val in ['else', endif_spelling]
    enders = Enders()
    
    while True:
        bits = token.split_contents()
        command = bits[0]
        bits = bits[1:]
        if command == if_spelling:
            message, user = parse(bits)
            nodelist = parser.parse(enders)
            next_token = parser.next_token()
            if_elifs.append((message, user, nodelist, token))
            if_spelling = 'elif'
            token = next_token
        elif token.contents == 'else':
            nodelist_false = parser.parse((endif_spelling,))
            parser.delete_first_token()
            break
        elif token.contents == endif_spelling:
            nodelist_false = template.NodeList()
            break
    while len(if_elifs) > 1:
        message, user, nodelist_true, token = if_elifs.pop()
        false_node = IfHasReadNode(message, user, nodelist_true, nodelist_false, negate)
        nodelist_false = parser.create_nodelist()
        parser.extend_nodelist(nodelist_false, false_node, token)
    message, user, nodelist_true, token = if_elifs[0]
    return IfHasReadNode(message, user, nodelist_true, nodelist_false, negate)

@register.tag
def ifhasread(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.

    Examples::

        {% ifhasread message for user %}
            ...
        {% endifhasread %}

        {% ifnothasread message for user %}
            ...
        {% elif message for user %}
            ...
        {% else %}
            ...
        {% endifnothasread %}
    """
    return do_ifhasread(parser, token, False)

@register.tag
def ifnothasread(parser, token):
    """
    Outputs the contents of the block if the user has permission of object.
    See ifhasperm.
    """
    return do_ifhasread(parser, token, True)