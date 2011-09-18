# -*- coding: utf-8 -*-
#
# Created:    2010/09/10
# Author:         alisue
#
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from libwaz.db.models import ModelWithRequest
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.trackback.utils import Trackback

from ..markitupfield.models import MarkItUpField

import datetime

class Category(ModelWithRequest):
    u"""ブログのカテゴリー"""
    label       = models.CharField(u"カテゴリー名", max_length=255)
    author      = models.ForeignKey(User, related_name='blog_categories', editable=False)
    
    class Meta:
        unique_together = (('author', 'label'),) 
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry-archive-category', (), {'author': self.author, 'category': self.label})
        
    def __unicode__(self):
        return self.label
    
    def save(self, request=None, *args, **kwargs):
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        super(Category, self).save(request, *args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.entries.clear()
        super(Category, self).delete(*args, **kwargs)
        
    def json(self):
        return {'pk': self.pk, 'label': self.label}
    
    def modify_object_permission(self, mediator, created):
        # Premission
        mediator.manager(self, self.author)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')
        
class EntryManager(models.Manager):
    def published(self, request):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
            q |= Q(pub_state='private', author=request.user)
        return self.filter(q).distinct().order_by('-publish_at')
    
    def draft(self, request):
        if not request or not request.user.is_authenticated():
            return self.none()
        else:
            return self.filter(pub_state='draft', author=request.user).order_by('-updated_at')
    
class Entry(ModelWithRequest):
    u"""ブログの記事"""
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['private'],
        settings.PUB_STATES['draft'],
    )
    pub_state       = models.CharField(
        u"公開設定",
        max_length=10,
        choices=PUB_STATES,
        default="public",
        help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES)
    )
    title           = models.CharField(u"タイトル", max_length=255)
    
    body            = MarkItUpField(u"本文", default_markup_type='markdown')
    category        = models.ForeignKey(
        Category,
        verbose_name=u"カテゴリー",
        related_name="entries",
        blank=True,
        null=True,
        help_text=u"ブログをカテゴリ分けして整理するのに利用してください。カテゴリを追加するには横のプラスボタンを押してください"
    )
    
    # Automatic Invisible field
    author          = models.ForeignKey(User, verbose_name=u"著者", related_name='blog_entries', editable=False)
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True, help_text=u"作成日時")
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True, help_text=u"更新日時")
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False, help_text=u"公開日時")
    publish_at_date = models.DateField(u"公開日", null=True, editable=False, help_text=u"公開日")
    
    tags            = TaggingField()
    
    objects         = EntryManager()
    
    class Meta:
        ordering            = ('-publish_at', 'title', '-updated_at')
        unique_together     = (('title', 'author', 'publish_at_date'),)
        verbose_name        = u"ブログ記事"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.title
    
    def clean(self, request=None):
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        if self.pub_state == 'draft' and self.publish_at:
            self.publish_at = None
            self.publish_at_date = None
        if self.pub_state != 'draft' and not self.publish_at:
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
        super(Entry, self).clean(request)
        
    def save(self, request=None, *args, **kwargs):
        super(Entry, self).save(request, *args, **kwargs)
        if self.pub_state != 'draft':
            pass
            # TODO: 動作確認
#            # 記事が公開されたのでTrackbackを送信
#            trackback = Trackback(
#                url=self.get_absolute_url(),
#                title=self.title,
#                excerpt=self.body.raw[:100],
#                blog_name=u"%sのブログ - Kawaz.tk" % self.author.get_profile().nickname
#            )
#            urls = Trackback.findurls(self.body.raw)
#            for url in urls:
#                trackback.ping(Trackback.autodiscover(url))
    
    def modify_object_permission(self, mediator, created):
        # Permission
        mediator.manager(self, self.author)
        if self.pub_state in ('draft', 'private'):
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        elif self.pub_state == 'protected':
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')
        
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('blogs-entry-update', (), {
                'author':       self.author,
                'object_id':    self.pk
            })
        else:
            return ('blogs-entry-detail', (), {
                'author':   self.author,
                'year':     self.publish_at.strftime('%Y'),
                'month':    self.publish_at.strftime('%m'),
                'day':      self.publish_at.strftime('%d'),
                'object_id':     self.pk,
            })
