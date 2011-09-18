# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/03
#
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.history import site

from ..bugwaz.models import Product as BugwazProduct

from ..defaultimg import get_default_project_icon
from ..imagefield.fields import ImageField
from ..markitupfield.models import MarkItUpField

import os
import datetime

class CategoryManager(models.Manager):
    def active(self):
        u"""
        最低でも一つのプロジェクトに紐づけられているCategoryのみ取得
        """
        from django.db.models import Count
        return self.annotate(projects_count=Count('projects')).exclude(projects_count=0).distinct()

    def get_by_natural_key(self, label):
        return self.get(label=label)
    
class Category(models.Model):
    u"""
    プロジェクトのカテゴリ
    """
    label   = models.CharField(u'カテゴリ名', max_length=32, unique=True)
    parent  = models.ForeignKey('self', verbose_name=u'親カテゴリ', null=True, blank=True, related_name='children')
    
    objects = CategoryManager()
    
    class Meta:
        ordering            = ('label',)
        verbose_name        = u"カテゴリ"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.label
    
    def delete(self):
        self.projects.clear()
        super(Category, self).delete()
        
    @models.permalink
    def get_absolute_url(self):
        return ('projects-project-list', (), {'category': self.label})

    def natural_key(self):
        return self.label
    
class ProjectManager(models.Manager):
    def related(self, request, user):
        if request and request.user.is_authenticated():
            qs = self.published(request)
            return qs.filter(members=user)
        else:
            return self.none()
    
    def published(self, request):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
            q |= Q(pub_state='group', group__in=request.user.groups.all())
        return self.filter(q).distinct()
    
    def draft(self, request):
        if request and request.user.is_authenticated():
            return self.filter(pub_state='draft', author=request.user)
        else:
            return self.none()
    
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
   
class Project(models.ModelWithRequest):
    u"""プロジェクト詳細モデル"""
    def _get_upload_path(self, filename):
        path = u'storage/projects/%s' % self.slug
        return os.path.join(path, filename)
    
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['draft'],
    )
    PERMISSIONS = (
         (u"protected",        u"コミュニティメンバー全員が記事編集可能"),
         (u"group",     u"プロジェクトメンバーのみが記事編集可能"),
         (u"private",       u"管理者のみが記事編集可能"),
    )
    STATUS = (
        (u"planning",    u"企画中"),
        (u"active",      u"活動中"),
        (u"paused",      u"一時停止中"),
        (u"eternal",     u"エターナった"),
        (u"done",        u"完成"),
    )
    
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    # Required
    pub_state       = models.CharField(u'公開設定', choices=PUB_STATES, max_length=10, default=u'public', help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    status          = models.CharField(u"ステータス", default="planning", max_length=15, choices=STATUS)
    permission      = models.CharField(u"権限", choices=PERMISSIONS, max_length=15, default=u"group", help_text=u"プロジェクトに属するWikiの編集権限です")
    title           = models.CharField(u"プロジェクト名", max_length=127, unique=True)
    slug            = models.SlugField(u"プロジェクトID", unique=True, max_length=63, 
                                       help_text=u"URLに使用される文字列です。設定後、変更することはできません。利用可能な文字は、英数字と_-のみです")
    body            = MarkItUpField(u"プロジェクト概要", default_markup_type='markdown')
    # Omittable
    icon            = ImageField(u"サムネイル", upload_to=_get_upload_path, blank=True, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS)
    category        = models.ForeignKey(Category, verbose_name=u'カテゴリ', null=True, blank=True, related_name='projects', 
                                        help_text=u"プロジェクトの分類に使用してください。使用したいカテゴリーが存在しない場合は運営に要求してください")
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=u"管理者", related_name="projects_owned", editable=False)
    updated_by      = models.ForeignKey(User, verbose_name=u"編集者", related_name="projects_updated", editable=False)
    members         = models.ManyToManyField(User, verbose_name=u"メンバー", related_name="projects_joined", editable=False)
    group           = models.ForeignKey(Group, verbose_name=u"グループ", unique=True, editable=False)
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    publish_at      = models.DateTimeField(u"公開日時", null=True, editable=False)
    publish_at_date = models.DateField(u"公開日", null=True, editable=False)
    bugwaz          = models.ForeignKey(BugwazProduct, verbose_name=u"Bugwaz", unique=True)
    
    tags            = TaggingField()
    
    objects         = ProjectManager()
    
    class Meta:
        app_label           = 'projects'
        ordering            = ('status', '-updated_at', 'title') 
        verbose_name        = u"プロジェクト"
        verbose_name_plural = verbose_name
        permissions = (
            ('add_wiki_project', 'Can add wiki on the project'),
            ('add_task_project', 'Can add task on the project'),
            ('add_thread_project', 'Can add thread on the project'),
            ('add_material_project', 'Can add material on the project'),
            ('join_project',    'Can join the project'),
            ('kick_project',    'Can kick the user in the project'),
        )
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('projects-project-update', (), {'object_id': self.pk})
        return ("projects-project-detail", (), {'slug': self.slug})
    
    def natural_key(self):
        return self.slug
    
    def clean(self, request=None):
        if self.pub_state == u'draft' and self.publish_at:
            # 下書きが公開日時を持っているのはおかしな話なので None 設定を行う
            self.publish_at = None
            self.publish_at_date = None
        if self.pub_state != u'draft' and not self.publish_at:
            # 下書きから公開設定にされたときに公開日時を現在時刻に設定する
            self.publish_at = datetime.datetime.now()
            self.publish_at_date = datetime.date.today()
        if self.pk is None:
            self.author = request.user if request else settings.SYSTEM_USER()
            # Uniqueチェックを先に行う
            if Project.objects.filter(Q(slug=self.slug)|Q(title=self.title)).exists():
                # すでに記事が存在しているためsuper().clean()にてエラーを投げてもらう
                super(Project, self).clean()
            # Groupの自動生成
            group = Group.objects.get_or_create(name=u"project_%s"%self.slug)[0]
            self.group = group
            # Bugwazを自動的に生成する
            bugwaz = BugwazProduct.objects.get_or_create(label=self.title, body=self.body, rules=u"", group=self.group)[0]
            self.bugwaz = bugwaz
        self.updated_by = request.user if request else settings.SYSTEM_USER()
        super(Project, self).clean()
    
    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        if not hasattr(self, 'group') or self.group is None:
            group = Group.objects.create(name=u"project_%s"%self.slug)
            self.group = group
            # Bugwazを自動的に生成する
            bugwaz = BugwazProduct.objects.create(label=self.title, body=self.body, rules=u"", group=self.group)
            self.bugwaz = bugwaz
        super(Project ,self).save(request, *args, **kwargs)
        # 更新履歴登録
        if action is None:
            site.get_backend(Project).autodiscover(self, action if action else created)
        # 作成後処理
        if created:
            self.join(self.author, save=False)
            self.save(request, action='ignore')
        # 全員がちゃんとグループに属していることを保証
        for member in self.members.all():
            member.groups.add(self.group)
        
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author, [
            'kick_project', 'add_wiki_project', 'add_task_project', 'add_thread_project', 'add_material_project'
        ])
        if self.pub_state == 'draft':
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
            mediator.reject(self, self.group)
        elif self.pub_state == 'public':
            mediator.viewer(self, 'anonymous')
            mediator.viewer(self, None, ['join_project'])
            mediator.editor(self, self.group, ['add_task_project', 'add_thread_project', 'add_material_project', 'join_project'])
        elif self.pub_state == 'protected':
            mediator.reject(self, 'anonymous')
            mediator.viewer(self, None, ['join_project'])
            mediator.editor(self, self.group, ['add_task_project', 'add_thread_project', 'add_material_project', 'join_project'])
        # Wiki編集権限
        if self.permission == 'protected':
            mediator.contribute(self, None, ['add_wiki_project'])
            mediator.contribute(self, self.group, ['add_wiki_project'])
        elif self.permission == 'group':
            mediator.contribute(self, self.group, ['add_wiki_project'])
        
    def join(self, user, save=True):
        self.members.add(user)
        user.groups.add(self.group)
        if save:
            self.save(request=None, action='join')
            site.get_backend(Project).autodiscover(self, 'join', user=user)
        
    def quit(self, user, save=True):
        if user == self.author:
            raise AttributeError("Author doesn't allow to quit the project")
        self.members.remove(user)
        user.groups.remove(self.group)
        if save:
            self.save(request=None, action='quit')
            site.get_backend(Project).autodiscover(self, 'quit', user=user)
        
    def get_icon_display(self, pattern_name=None):
        kwargs = {
            'status':   self.status,
            'alt':      u"%sのアイコン"%self.title,
            'title':    u"%sの詳細を見る"%self.title,
        }
        if self.icon:
            kwargs['src'] = self.icon.url if not pattern_name else getattr(self.icon, pattern_name).url
        else:
            kwargs['src'] = get_default_project_icon(pattern_name, self.pk)
        return mark_safe(
            u"""<img class="project-status-%(status)s" src="%(src)s" alt="%(alt)s" title="%(title)s" />""" %kwargs)
    get_icon_small_display = lambda self: self.get_icon_display('small')
    get_icon_middle_display = lambda self: self.get_icon_display('middle')
    get_icon_large_display = lambda self: self.get_icon_display('large')
    get_icon_huge_display = lambda self: self.get_icon_display('huge')
    
    def get_title_display(self):
        kwargs = {
            'href':     self.get_absolute_url(),
            'title':   self.title,
            'title2':    u"%sの詳細を見る"%self.title,
        }
        return mark_safe(u"""<a href="%(href)s" title="%(title2)s">%(title)s</a>""" % kwargs)