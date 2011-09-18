# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.object_permission import ObjectPermissionMediator
from libwaz.contrib.history import site

from ..projects.models import Project
from ..markitupfield.models import MarkItUpField
import status

import datetime

class TaskManager(models.Manager):
    def published(self, request=None):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
            q |= Q(pub_state='group', project__group__in=request.user.groups.all())
        return self.filter(q).distinct()
    
    def draft(self, request=None):
        if request and request.user.is_authenticated():
            return self.filter(pub_state='draft', author=request.user)
        else:
            return self.none()
    
    def active(self, request=None):
        if request and request.user.is_authenticated():
            qs = self.published(request)
            qs = qs.exclude(status='close')
            return qs
        else:
            return self.none()
    
    def relative(self, request, user):
        if request and request.user.is_authenticated():
            qs = self.active(request)
            return qs.filter(Q(author=user) | Q(owners=user))
        else:
            return self.none()

class Task(models.ModelWithRequest):
    u"""プロジェクト内で発行されたタスクのモデル"""
    STATUSES = status.STATUSES
    
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['group'],
        settings.PUB_STATES['draft']
    )
    PRIORITIES = (
        (5,             u'緊急'),
        (4,             u'最優先'),
        (3,             u'優先'),
        (2,             u'やや低い'),
        (1,             u'低い'),
    )
    # Required
    pub_state       = models.CharField(u"公開設定", max_length=10, choices=PUB_STATES, default="public", help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    title           = models.CharField(u"タイトル", max_length=255, help_text=u"タスクの名称です。一覧などに表示されるためわかりやすい名前を指定してください")
    body            = MarkItUpField(u"詳細", default_markup_type='markdown')
    # unrequired
    status          = models.CharField(u"ステータス", choices=status.STATUSES, max_length=15, default="new", 
                                       help_text=u"タスクの状態です。タスクの進行度合いなどを表現します")
    priority        = models.IntegerField(u"優先度", choices=PRIORITIES, default=3, help_text=u"タスクの優先度です")
    deadline        = models.DateField(u"締切", null=True, blank=True, 
                                       help_text=u"タスクの締切りです。締切りがあるタスクで指定してください")
    owners          = models.ManyToManyField(User, verbose_name="担当者", related_name="tasks_charged", null=True, blank=True, 
                                             help_text=u"タスクの担当者です。プロジェクトが選択されている場合はプロジェクトメンバーのみが表示されます。")
    # Uneditable
    project         = models.ForeignKey(Project, verbose_name="所属プロジェクト", related_name="tasks", null=True, blank=True,
                                        help_text=u"タスクを所属させるプロジェクトです。プロジェクトを指定すると担当者がプロジェクトメンバー以外指定できなくなります")
    author          = models.ForeignKey(User, verbose_name="発行者", editable=False, related_name="tasks_owned")
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateField(u"公開日", null=True, editable=False)
    
    tags            = TaggingField()
    
    objects         = TaskManager()
    
    class Meta:
        ordering            = ('status', 'deadline', 'priority', '-updated_at')
        unique_together     = (('project', 'title'), ('author', 'title'),)
        verbose_name        = u"タスク"
        verbose_name_plural = verbose_name
        permissions = (
            ('status_task',     'Can change status of the task'),
        )
        
    def __unicode__(self):
        if self.project:
            return u"%s - %s" % (self.title, self.project)
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        kwargs = {'object_id': self.pk}
        if self.pub_state == 'draft':
            return ('tasks-task-update', (), kwargs)
        return  ('tasks-task-detail', (), kwargs)
    
    def clean(self, request):
        created = self.pk is None
        if created:
            # 新規作成時限定で締切りのValidation
            if self.deadline and self.deadline < datetime.date.today():
                raise ValidationError(u"締め切りは現在より先の日付である必要があります。")
            # 著者の自動設定
            self.author = request.user if request else settings.SYSTEM_USER()
        # 公開範囲のValidation
        if not self.project and self.pub_state == 'group':
            raise ValidationError(u"プロジェクトを指定しない状態でパーミッションをグループに設定できません")
        # 下書き関係のValidation
        if self.pub_state == 'draft' and self.publish_at:
            self.publish_at = None
            self.publish_at_date = None
        elif self.pub_state != 'draft' and not self.publish_at:
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
    
    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        super(Task, self).save(request, *args, **kwargs)
        if action is None:
            site.get_backend(Task).autodiscover(self, created)
        else:
            site.get_backend(Task).autodiscover(self, action)
            
    def modify_object_permission(self, mediator, created, **kwargs):
        mediator.manager(self, self.author, ['tasks.status_task'])
        if self.pub_state == 'draft':
            mediator.reject(self, None)
            if self.project:
                mediator.reject(self, self.project.group)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        elif self.pub_state == 'protected':
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'group':
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
            mediator.viewer(self, self.project.group)
    
    def modify_object_permission_m2m(self, mediator, sender, model, pk_set, removed):
        if sender == self.owners.through:
            for owner in model.objects.filter(pk__in=pk_set):
                if owner == self.author:
                    continue
                elif not removed:
                    mediator.viewer(self, owner, ['tasks.status_task'])
                else:
                    mediator.discontribute(self, owner, ['tasks.status_task'])
    
    def join(self, user):
        if self.project and not user in self.project.members.all():
            raise ValidationError(u"プロジェクト指定時は担当者がプロジェクトに所属している必要があります")
        self.owners.add(user)
        self.save(request=None, action='join')
        
    def quit(self, user):
        self.owners.remove(user)
        self.save(request=None, action='quit')
        
    def get_status_display(self):
        return status.STATUSES_DICT[self.status]
    
    def get_avariable_status_list(self, user):
        is_author = user == self.author
        is_owner = user in self.owners.all()
        status_list = []
        if self.status == status.NEW:
            if is_owner:
                status_list = [status.ACCEPTED, status.CANCELED]
        elif self.status == status.CANCELED:
            pass
        elif self.status == status.ACCEPTED:
            if is_owner:
                status_list = [status.PAUSED, status.DONE, status.CANCELED]
        elif self.status == status.REJECTED:
            if is_owner:
                status_list = [status.ACCEPTED, status.CANCELED]
        elif self.status == status.PAUSED:
            if is_owner:
                status_list = [status.ACCEPTED, status.DONE, status.CANCELED]
        elif self.status == status.DONE:
            if is_owner:
                status_list = [status.ACCEPTED, status.CANCELED]
        elif self.status == status.FROZEN:
            if is_owner:
                status_list = [status.CANCELED]
        elif self.status == status.CLOSED:
            pass
        if is_author:
            if self.status == status.NEW:
                pass
            elif self.status == status.CANCELED:
                pass
            elif self.status == status.FROZEN:
                # Note: 必ず誰かが一度はAcceptedにしている
                status_list = [status.ACCEPTED, status.CLOSED]
            elif self.status == status.CLOSED:
                # Note: 必ず誰かが一度はAccpetedにしている
                status_list = [status.REJECTED]
            else:
                status_list += [status.FROZEN, status.CLOSED]
        return status_list