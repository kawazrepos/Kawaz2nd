# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from ..projects.models import Project
from ..mcomments.models import MarkItUpComment
from ..markitupfield.models import MarkItUpField

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.history import site

import datetime

class ThreadManager(models.Manager):
    def published(self, request=None):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
            q |= Q(pub_state='group', project__group__in=request.user.groups.all())
        return self.filter(q)
    
    def draft(self, request=None):
        if request and request.user.is_authenticated():
            return self.filter(pub_state='draft', author=request.user)
        else:
            return self.none()
        
class Thread(models.ModelWithRequest):
    u"""スレッド詳細モデル"""
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['group'],
        settings.PUB_STATES['draft']
    )
    COMMENT_PERMISSIONS = (
        ('public',      u"全てのユーザーが返信可能"),
        ('protected',   u"コミュニティメンバーのみ返信可能"),
        ('group',       u"プロジェクトメンバーのみ返信可能"),
    )
    # Required
    pub_state       = models.CharField(u"公開設定", default="public", max_length=15, choices=PUB_STATES, help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    permission      = models.CharField(u"書き込み権限", default="public", max_length=15, choices=COMMENT_PERMISSIONS)
    title           = models.CharField(u"タイトル", max_length=127)
    body            = MarkItUpField(u"本文", default_markup_type='markdown')
    # Omittable
    project         = models.ForeignKey(Project, verbose_name="所属プロジェクト", null=True, blank=True, related_name="threads")
    # Uneditaqble
    author          = models.ForeignKey(User, verbose_name=u"スレッドオーナー", editable=False, related_name="threads")
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateField(u"公開日", null=True, editable=False)
    
    tags            = TaggingField()
    
    objects         = ThreadManager()
    
    class Meta:
        ordering            = ('-updated_at', '-publish_at', 'title')
        unique_together     = (('project', 'title'),)
        verbose_name        = u"スレッド"
        verbose_name_plural = verbose_name
        permissions = (
            ('comment_thread',  'Can comment on the thread'),
        )
        
    def __unicode__(self):
        if self.project:
            return u"%s - %s" % (self.title, self.project)
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('threads-thread-update', (), {'object_id': self.pk})
        else:
            return ("threads-thread-detail", (), {'object_id':self.pk})

    def clean(self, request=None):
        u"""各種Validation及び著者の自動設定"""
        if self.pub_state == 'draft' and self.publish_at:
            # 下書きが公開日時を持っているのはおかしな話なので None 設定を行う
            self.publish_at = None
            self.publish_at_date = None
        if self.pub_state != 'draft' and not self.publish_at:
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
        if self.pub_state == 'group' and self.permission != 'group':
            raise ValidationError(u"公開設定に対して、書き込み権限が不正です")
        elif self.pub_state == 'protected' and self.permission == 'public':
            raise ValidationError(u"公開設定に対して、書き込み権限が不正です")
        if self.pub_state == 'group' and not self.project:
            raise ValidationError(u"プロジェクトに所属していないスレッドはプロジェクト内のみ公開にできません")
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        super(Thread, self).clean()
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author, ['threads.comment_thread'])
        if self.pub_state == 'draft':
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'group':
            if self.project:
                mediator.viewer(self, self.project.group, ['threads.comment_thread'])
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'protected':
            if self.project:
                mediator.viewer(self, self.project.group, ['threads.comment_thread'])
            mediator.viewer(self, None, ['threads.comment_thread'] if self.permission != 'group' else [])
            mediator.reject(self, 'anonymous')
        else:
            if self.project:
                mediator.viewer(self, self.project.group, ['threads.comment_thread'])
            mediator.viewer(self, None, ['threads.comment_thread'] if self.permission != 'group' else [])
            mediator.viewer(self, 'anonymous', ['threads.comment_thread'] if self.permission == 'public' else [])
    
    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        super(Thread, self).save(request, *args, **kwargs)
        if action is None:
            site.get_backend(Thread).autodiscover(self, created)
        
    def response(self):
        ct = ContentType.objects.get_for_model(self)
        qs = MarkItUpComment.objects.filter(content_type=ct, object_pk=self.pk)
        return qs

#
# Notice:
#    コメントが投稿されたときにsaveを呼び出し`updated_at`を
#    自動的に更新する
from django.db.models import signals
def _post_save_callback(sender, instance, created, **kwargs):
    if isinstance(instance.content_object, Thread):
        instance.content_object.save(request=None, action='update')
signals.post_save.connect(_post_save_callback, sender=MarkItUpComment)