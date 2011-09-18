# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User

from libwaz.db import models
from ..markitupfield.models import MarkItUpField

import datetime

class AnnouncementManager(models.Manager):
    def published(self, request):
        if request and request.user.is_authenticated():
            return self.exclude(pub_state='draft')
        else:
            return self.filter(pub_state='public')
    def draft(self, request):
        if request and request.user.is_authenticated():
            return self.filter(pub_state='draft', author=request.user)
        else:
            return self.none()
        
class Announcement(models.ModelWithRequest):
    u"""
    An announcement that came from staff user
    """
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['draft'],
    )
    # Required
    pub_state       = models.CharField(u"公開範囲", max_length=10, choices=PUB_STATES, 
                                       help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES), default='public')
    title           = models.CharField(u"タイトル", max_length=128)
    body            = MarkItUpField(u"本文", default_markup_type='markdown')
    sage            = models.BooleanField(u"Sage", default=False, 
                                          help_text=u"チェックを入れるとトップページのお知らせに表示させません。"
                                                    u"また各ユーザーに対する通知も飛ばしません")
    # Uneditable
    author          = models.ForeignKey(User, related_name='created_announcements')
    updated_by      = models.ForeignKey(User, related_name='updated_announcements')
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateField(u"公開日", null=True, editable=False)
    objects         = AnnouncementManager()
    
    class Meta:
        ordering            = ('-created_at',)
        verbose_name        = u"お知らせ"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ("announcements-announcement-update", (), {'object_id': self.pk})
        return ("announcements-announcement-detail", (), {'object_id':self.pk})
    
    def clean(self, request=None, *args, **kwargs):
        created = self.pk is None
        if created:
            # 著者の自動設定
            self.author = request.user if request else settings.SYSTEM_USER()
        # 下書き関係のValidation
        if self.pub_state == 'draft' and self.publish_at:
            self.publish_at = None
            self.publish_at_date = None
        elif self.pub_state != 'draft' and not self.publish_at:
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
        # 更新者の自動設定
        self.updated_by = request.user if request else settings.SYSTEM_USER()
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author)
        if self.pub_state == 'draft':
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'protected':
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')
        else:
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')