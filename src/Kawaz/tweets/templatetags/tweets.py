# -*- coding:utf-8 -*-
from django import template
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe

from ...templatetags.templatetags import parser
from ..models import Tweet

import re

register = template.Library()

class GetTweetsForAs(template.Node):
    def __init__(self, user, variable_name):
        self.user, self.variable_name = user, variable_name
    
    def render(self, context):
        qs = Tweet.objects.all()
        if self.user:
            user = self.user.resolve(context)
            qs = qs.filter(author=user)
        context[self.variable_name] = qs
        return ''

@register.tag
def get_tweets(parser, context):
    u"""
    Usage:
        get_tweets (for <user>) as <variable>
    """
    bits = context.split_contents()
    
    if len(bits) == 5:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError(u"first argument of %r has to be 'for'" % bits[0])
        elif bits[3] != 'as':
            raise template.TemplateSyntaxError(u"third argument of %r has to be 'as'" % bits[0])
        user = parser.compile_filter(bits[2])
        variable_name = bits[4]
    elif len(bits) == 3:
        if bits[1] != 'as':
            raise template.TemplateSyntaxError(u"first argument of %r has to be 'as'" % bits[0])
        user = None
        variable_name = bits[2]
    else:
        raise template.TemplateSyntaxError(u"%r has to be written like 'get_tweets (for <user>) as <variable>'" % bits[0])
    return GetTweetsForAs(user, variable_name)

@register.filter
def tweettimesince(value):
    since = datetime.now() - value
    if since < timedelta(minutes=1):
        return u"%d秒前" % since.seconds
    elif since < timedelta(hours=1):
        return u"%d分前" % (since.seconds/60)
    elif since < timedelta(days=1):
        return u"約%d時間前" % (since.seconds/3600)
    elif since < timedelta(days=7):
        return u"約%d日前" % since.days
    else:
        return value.strftime("%m月%d日(%a) %H時%M分")

@register.filter
def parse_tweet(value):
    #value = re.sub(r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)', '<a href="\g<0>" rel="external">\g<0></a>', value)
    value = re.sub(r'http://(yfrog|twitpic).com/(?P<id>\w+/?)', '', value)
    value = re.sub(r'#(?P<tag>\w+)', '<a href="http://search.twitter.com/search?tag=\g<tag>" rel="external">#\g<tag></a>', value)
    value = parser.parse(value, full=False)
    #value = re.sub(r'@(?P<username>\w+)', '@<a href="http://twitter.com/\g<username>/" rel="external">\g<username></a>', value)
    
    return mark_safe(value)

def tweet_attachments(ex, value, max_items = -1):
    start = 0
    matches = ex.search(value, start)
    ids = []
    
    while matches:
        groupdict = matches.groupdict()
        if 'id' in groupdict:
            if not groupdict['id'] in ids:
                ids.append(groupdict['id'])
        
        start = matches.end()
        matches = ex.search(value, start)
    
    if max_items > -1:
        ids = ids[:max_items]
    
    return ids

@register.simple_tag
def yfrog_images(value, max_items = -1, lightbox = None):
    ex = re.compile(r'http://yfrog.com/(?P<id>\w+/?)')
    ids = tweet_attachments(ex, value, max_items)
    
    classes = ['yfrog-thumbnail']
    if lightbox:
        classes += [lightbox]
        extension = ':iphone'
    else:
        extension = ''
    
    urls = '\n'.join(
        [
            '<a href="http://yfrog.com/%(id)s%(extension)s" class="%(classes)s" rel="lightbox"><img src="http://yfrog.com/%(id)s.th.jpg" class="configured" /></a>' % {
                'id': i,
                'classes': ' '.join(classes),
                'extension': extension
            } for i in ids
        ]
    )
    
    return mark_safe(urls)

@register.simple_tag
def twitpic_images(value, max_items = -1, lightbox = None):
    ex = re.compile(r'http://twitpic.com/(?P<id>\w+/?)')
    ids = tweet_attachments(ex, value, max_items)
    
    classes = ['twitpic-thumbnail']
    if lightbox:
        classes += [lightbox]
    
    urls = '\n'.join(
        [
            '<a href="http://twitpic.com/show/full/%(id)s" class="%(classes)s" rel="lightbox"><img src="http://twitpic.com/show/thumb/%(id)s" class="configured" /></a>' % {
                'id': i,
                'classes': ' '.join(classes),
            } for i in ids
        ]
    )

    return mark_safe(urls)