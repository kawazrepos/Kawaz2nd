# vim: set fileencoding=utf-8 :
"""
Views of


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
from __future__ import with_statement
from random import choice
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from Kawaz.tweets.models import Tweet

ADAM_TWEETS = (
    u'問題ない',
    u'そのためのネルフです',
    u'乗るなら早くしろ、でなければ帰れ',
    u'最優先事項だ',
    u'人は思い出を忘れることで生きてゆける だが決して忘れてはいけないものもある',
    u'自分の願望は、あらゆる犠牲を払い、自分の力で実現させるものだ。他人から与えられるものではない',
    u'時計の針は元には戻らない。だが、自らの手で進めることは出来る',
    u'所詮、人間の敵は人間だよ',
    u'俺と一緒に人類の新たな歴史を作らないか？',
    u'かつて誰もが成し得なかった神への道。人類補完計画だよ',
    u'構わん、やれ',
)

@require_http_methods(['POST'])
def post_goforit(request):
    if not request.user.has_perm('auth.post_goforit'):
        return HttpResponseForbidden(u"")
    Tweet.objects.create(
        body=choice(ADAM_TWEETS),
        reply=None,
        author=request.user,
        source='kawaz',
    )
    return redirect("/")

