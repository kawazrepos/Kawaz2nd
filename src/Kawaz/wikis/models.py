# -*- coding:utf-8 -*-
from libwaz.db import models
from libwaz.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User

from libwaz.contrib.tagging.fields import TaggingField
from ..markitupfield.models import MarkItUpField
from ..projects.models import Project

import datetime

class WikiEntryManager(models.Manager):
    def published(self, request):
        filter = Q(pub_state='public')
        if request and request.user.is_authenticated():
            filter |= Q(pub_state='protected')
            filter |= Q(pub_state='group', project__group__in=request.user.groups.all())
        return self.filter(filter).distinct()
        
    def draft(self, request):
        if request.user.is_authenticated():
            return self.filter(author=request.user, pub_state='draft')
        else:
            return self.none()
    
class Entry(models.ModelWithRequest):
    u"""Wikiエントリーモデル"""
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['group'],
        settings.PUB_STATES['draft'],
    )
    PERMISSIONS = (
          (u'inherit',  u"プロジェクトの設定を引き継ぐ"),
    ) + Project.PERMISSIONS
    # Required
    project         = models.ForeignKey(Project, verbose_name=u"プロジェクト", related_name="wiki_entries")
    pub_state       = models.CharField(u"公開範囲", default="public", choices=PUB_STATES, max_length=15, help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    permission      = models.CharField(u"権限", choices=PERMISSIONS, max_length=15, default=u"inherit", help_text=u"記事の編集権限です")
    # URLに日本語を変換する際にUnicodeの%変換されるため28文字以上だとURLFieldに入らなくなる
    title           = models.CharField(u"記事名", max_length=28, help_text=u"URLにも使用されるため可能な限り変更しないことをおすすめします（リンク切れを防ぐため）")
    body            = MarkItUpField(u"本文", default_markup_type='markdown')
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=u"ページ作成者", related_name="wiki_entries_owned", editable=False)
    updated_by      = models.ForeignKey(User, verbose_name=u"ページ更新者", related_name="wiki_entries_updated", editable=False)
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateTimeField(u"公開日", null=True, editable=False)
    
    tags            = TaggingField(related_name='wikis_entry_set')
    
    objects         = WikiEntryManager()
    
    class Meta:
        ordering            = ('-updated_at', '-publish_at', 'title',)
        unique_together     = (('project', 'title'),)
        verbose_name        = u"ウィキ記事"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return u"%s - %s" % (self.title, self.project)
    
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ("wikis-entry-update", (), {'project': self.project.slug, 'slug': self.title})
        return ("wikis-entry-detail", (), {'project': self.project.slug, 'slug': self.title})
    
    def clean(self, request=None):
        if self.pub_state == 'draft' and self.publish_at:
            # 下書きが公開日時を持っているのはおかしな話なので None 設定を行う
            self.publish_at= None
            self.publish_at_date = None
        if self.pub_state != 'draft' and not self.publish_at:
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
        self.updated_by = request.user if request else User.objects.get(pk=1)
        super(Entry, self).clean()
    
    def get_permission(self):
        if self.permission == 'inherit':
            return self.project.permission
        return self.permission
    
    def modify_object_permission(self, mediator, created):
        permission = self.get_permission()
        mediator.manager(self, self.author)
        if self.pub_state == 'draft':
            mediator.reject(self, None)
            mediator.reject(self, self.project.group)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'protected':
            mediator.reject(self, 'anonymous')
            if permission == 'protected':
                mediator.manager(self, None)
            elif permission == 'group':
                mediator.manager(self, self.project.group)
                mediator.viewer(self, None)
            elif permission == 'private':
                mediator.viewer(self, self.project.group)
                mediator.viewer(self, None)
        elif self.pub_state == 'group':
            mediator.reject(self, 'anonymous')
            mediator.reject(self, None)
            if permission != 'private':
                mediator.manager(self, self.project.group)
            else:
                mediator.viewer(self, self.project.group)
        elif self.pub_state == 'public':
            mediator.viewer(self, 'anonymous')
            if permission == 'protected':
                mediator.manager(self, None)
            elif permission == 'group':
                mediator.manager(self, self.project.group)
                mediator.viewer(self, None)
            elif permission == 'private':
                mediator.viewer(self, self.project.group)
                mediator.viewer(self, None)
                
def make_index(sender, instance, created, **kwargs):
    u"""プロジェクトが生成されたときに、自動的にindexページを作る"""
    from django.template.loader import render_to_string
    if created:
        body = render_to_string('wikis/default-index.mkd', {'project': instance})
        Entry.objects.create(
            project=instance,
            title='index',
            body=body,
            author=instance.author,
            updated_by=instance.author)
         
from django.db.models.signals import post_save
post_save.connect(make_index, sender=Project)
