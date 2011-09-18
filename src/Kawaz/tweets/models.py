# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from libwaz.db import models

from utils import post_tweet_to_twitter, post_twitter_with_bot

import datetime

class Tweet(models.ModelWithRequest):
    u"""つぶやき詳細モデル"""
    SOURCES = (
        (u'kawaz',    u'Kawaz'),
        (u'twitter',  u'Twitter'),
        (u'api',      u'API'),
    )
    # Required
    body            = models.CharField(u"本文", max_length=255, help_text=u"本文")
    # Omittable
    reply           = models.ForeignKey('self', verbose_name=u"リプライ先のTweet", blank=True, null=True)
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=u"投稿者", related_name='tweets', editable=False)
    users           = models.ManyToManyField(User, verbose_name="ふぁぼったユーザー", related_name='tweets_favorited', editable=False)
    source          = models.CharField(u"投稿元", max_length=127, choices=SOURCES)
    created_at      = models.DateTimeField(u"作成日時")
    
    twitter_id      = models.BigIntegerField(u"Twitter Status ID", null=True, editable=False, unique=True)
    
    class Meta:
        ordering            = ('-created_at',)
        verbose_name        = u"つぶやき"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return u"%s (%s)" % (
            self.body, self.author
        )                   
        
    def clean(self, request=None):
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        super(Tweet, self).clean()
    
    def save(self, request=None, *args, **kwargs):
        created = self.pk is None
        if created and not hasattr(self, 'created_at') or self.created_at is None:
            # Twitterからの場合はTwitterの物がセットされているため
            # auto_now=Trueを使っていない
            self.created_at = datetime.datetime.now()
        super(Tweet, self).save(request, *args, **kwargs)
        if created and self.source == 'kawaz':
            post_tweet_to_twitter(self)
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author)
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
        
    @models.permalink
    def get_absolute_url(self):
        return ("tweets-tweet-detail", (), {'author': self.author.username,'object_id': self.id})

#
# Historyの更新情報をTwitterにリダイレクト
from libwaz.contrib.history.models import Timeline
from django.db.models import signals
def post_timeline_to_twitter(timeline, max_length=70):
    import twitter.utils
    body = strip_tags(timeline.get_message())
    if len(body) > max_length:
        body = body[:max_length] + u"…"
    # URLはドメインを含まないため付加
    site = Site.objects.get_current()
    url = u"http://%s%s" %  (site.domain, timeline.get_absolute_url())
    # URL短縮
    url = twitter.utils.shorten(url)
    # 投稿
    post_twitter_with_bot(u"%s %s" % (body, url))
def post_save_callback(sender, instance, created, **kwargs):
    if created:
        post_timeline_to_twitter(instance)

if settings.TWITTER_ENABLE:
    signals.post_save.connect(post_save_callback, sender=Timeline)