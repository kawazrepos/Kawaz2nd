# -*- coding: utf-8 -*-
#
# @date:        2010/10/18
# @author:    alisue
#
u"""
指定された文字列内に存在する<a>タグを調べ
プレイヤーを表示可能ならばHTMLを変換して
返すフィルター群
"""

from django import template
from django.utils.safestring import mark_safe

import re

YOUTUBE_PATTERN = r"""<a\W*href=["']http:\/\/www.youtube.com/watch\?v=(?P<id>[a-zA-Z0-9_\-]+)["'].*>.*</a>"""
NICONICO_PATTERN = r"""<a\W*href=["']http:/\/\www.nicovideo.jp\/watch\/(?P<id>[a-z]{2}[0-9]+)\/?["'].*>.*</a>"""
USTREAM_PATTERN = r"""<a\W*href=["']http:/\/\www.ustream.tv\/recorded\/(?P<id>[0-9]+)\/?["'].*>.*</a>"""


register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def youtube(value):
    def repl(m):
        html = u"""<object class="viewer youtube">
            <param name="movie" value="http://www.youtube.com/v/%(id)s?fs=1&amp;hl=ja_JP"></param>
            <param name="allowFullScreen" value="true"></param>
            <param name="allowscriptaccess" value="always"></param>
            <embed src="http://www.youtube.com/v/%(id)s?fs=1&amp;hl=ja_JP" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true">
            </embed>
            </object>""" % m.groupdict()
        return html
    value = re.sub(YOUTUBE_PATTERN, repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def niconico(value):
    def repl(m):
        html = u"""<script type="text/javascript" src="http://ext.nicovideo.jp/thumb_watch/%(id)s"></script>
            <noscript><a href="http://www.nicovideo.jp/watch/%(id)s">動画を見る</a></noscript>""" % m.groupdict()
        return html
    value = re.sub(NICONICO_PATTERN, repl, value)
    return mark_safe(value)

@register.filter
@template.defaultfilters.stringfilter
def ustream(value):
    def repl(m):
        html = u"""<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="480" height="296" id="utv192095" name="utv_n_321660">
        <param name="flashvars" value="loc=%%2F&amp;autoplay=false&amp;vid=%(id)s&amp;locale=ja_JP&amp;hasticket=false&amp;id=%(id)s&amp;v3=1" />
        <param name="allowfullscreen" value="true" />
        <param name="allowscriptaccess" value="always" />
        <param name="src" value="http://www.ustream.tv/flash/viewer.swf" />
        <embed flashvars="loc=%%2F&amp;autoplay=false&amp;vid=%(id)s&amp;locale=ja_JP&amp;hasticket=false&amp;id=%(id)s&amp;v3=1" width="480" height="296" allowfullscreen="true" allowscriptaccess="always" id="utv192095" name="utv_n_321660" src="http://www.ustream.tv/flash/viewer.swf" type="application/x-shockwave-flash" />
        </object>""" % m.groupdict()
        return html
    value = re.sub(USTREAM_PATTERN, repl, value)
    return mark_safe(value)
        

@register.filter
@template.defaultfilters.stringfilter
def viewer(value):
    value = youtube(value)
    value = niconico(value)
    value = ustream(value)
    return mark_safe(value)
