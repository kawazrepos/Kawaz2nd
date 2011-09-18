# -*- coding: utf-8 -*-
#    
#    
#    created by giginet on 2011/07/20
#
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext

def is_spam(model, instance, body, author_name, request):
    u"""
        Spam checking using Akismet.
        @see http://djangosnippets.org/snippets/1255/
    """
    if not body or not author_name: return
    # spam checking can be enabled/disabled per the comment's target Model
    #if comment.content_type.model_class() != Entry:
    #    return
    try:
        from akismet import Akismet
    except:
        return
    
    # use TypePad's AntiSpam if the key is specified in settings.py
    if hasattr(settings, 'TYPEPAD_ANTISPAM_API_KEY'):
        ak = Akismet(
            key=settings.TYPEPAD_ANTISPAM_API_KEY,
            blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )
        ak.baseurl = 'api.antispam.typepad.com/1.1/'
    else:
        ak = Akismet(
                     key=settings.AKISMET_API_KEY,
                     blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )
    if ak.verify_key():
        data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': author_name.encode('utf-8'),
        }

        return ak.comment_check(body.encode('utf-8'), data=data, build_data=True)
    return False

def on_comment_will_be_posted(sender, comment, request, *args, **kwargs):
    if is_spam(sender, comment, comment.comment.raw, comment.user_name, request):
        # スパムコメントを投稿しようとしたとき、
        # 強制的に値を無効化してバリデーションを通らなくする
        # そして強制的にリダイレクト
        comment.is_public = False
        msg = ugettext("The %(verbose_name)s was created unsuccessfully.") %\
                                    {"verbose_name": sender._meta.verbose_name}
        messages.error(request, msg, fail_silently=True)
        referer = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer)
        