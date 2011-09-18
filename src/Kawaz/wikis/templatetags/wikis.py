# -*- coding: utf-8 -*-
#
# @author:    alisue
# @date:        2010/10/24
#
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.text import force_unicode
import re

register = template.Library()

WIKILINK = re.compile(r'(?P<prefix>[^\\])\[\[(?P<value>[^\]]*)\]\]')
NON_WIKILINK = re.compile(r'\\(\[\[[^\]]*\]\])')
@register.filter
def wikilinks(source, args):
    u"""
    [[名前]]という部分をWiki内リンクに変換するためのフィルタ
    \[[名前]]の場合はリンクにしない
    """
    html_class = u'wikilink'
    def repl(m):
        prefix = m.group("prefix")
        value = m.group("value")
        
        try:
            url = reverse('wikis-entry-detail', kwargs={'project': args.project.slug, 'slug': value})
            return u"""%(prefix)s<a href="%(url)s" class="%(class)s">%(value)s</a>""" % {
                'prefix': prefix,
                'url': url,
                'class': html_class,
                'value': value
            }
        except:
            return m.group(0)
    value = force_unicode(source)
    value = re.sub(WIKILINK, repl, value)
    value = re.sub(NON_WIKILINK, r'\1', value)
    return mark_safe(value)
