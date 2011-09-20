# -*- coding:utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from libwaz.db import models
from libwaz.db.models import Q
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.history import site

from ..projects.models import Project
from utils import filetypes, html

import os.path
import mimetypes
import datetime

class MaterialManager(models.Manager):
    def published(self, request):
        q = Q(pub_state='public')
        if request and request.user.is_authenticated():
            q |= Q(pub_state='protected')
            q |= Q(pub_state='group', project__group__in=request.user.groups.all())
        return self.filter(q).distinct()
    
    def commons(self, request):
        return self.published(request).exclude(license='reject')
    
class Material(models.ModelWithRequest):
    u"""コモンズ素材モデル"""
    def _get_upload_path(self, filename):
        path = u'storage/commons/%(user)s/' % {
            'user':    self.author,
        }
        return os.path.join(path, filename)
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
        settings.PUB_STATES['group'],
    )
    LICENSES = (
        ('for-profit',                  u'営利利用可能'),
        ('for-personal',                u'非営利のみ可能'),
        ('commercial-under-permitted',  u'営利のみ許可必須'),
        ('restrict',                    u'素材利用を許可しない(閲覧のみを許可)'),
        ('reject',                      u'ダウンロードを許可しない'),
    )
    # Required
    pub_state   = models.CharField(u"公開範囲", max_length=10, choices=PUB_STATES, default='public', help_text=settings.PUB_STATE_HELP_TEXT(PUB_STATES))
    license     = models.CharField(u"ライセンス", max_length=32, choices=LICENSES, default='for-profit',
                                   help_text=u"ダウンロードを許可しない設定にするとダウンロードが不可となります。ダウンロードを許可しない設定でも画像・動画・音声のプレビューは可能です")
    file        = models.FileField(u"ファイル", upload_to=_get_upload_path)
    # Unrequired
    title       = models.CharField(u"タイトル", max_length=127, blank=True)
    body        = models.TextField(u"概要", blank=True)
    # Hidden
    project     = models.ForeignKey(Project, verbose_name=u'所属プロジェクト', related_name="materials", blank=True, null=True)
    # Uneditable
    author      = models.ForeignKey(User, related_name="materials", editable=False)
    ip_address  = models.IPAddressField(u"IP Address", editable=False)
    pv          = models.PositiveIntegerField(u"ダウンロード回数", default=0, editable=False)
    created_at  = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at  = models.DateTimeField(u"更新日時", auto_now=True)
    
    tags        = TaggingField()
    
    objects     = MaterialManager()
    
    class Meta:
        ordering            = ('-updated_at', '-created_at')
        verbose_name        = u"素材"
        verbose_name_plural = verbose_name
        permissions         = (
            ('view-pv_material', 'Can view pv of material'),
            ('view-ip_material', 'Can view ip of material'),
        )
        
    def __unicode__(self):
        if self.project:
            return u"%s - %s" % (self.title, self.project)
        return self.title
    
    def clean(self, request=None):
        if self.pk is None:
            self.author = request.user if request else User.objects.get(pk=1)
            self.ip_address = request.META['REMOTE_ADDR']  if request else "127.0.0.1"
        # 公開範囲のValidation
        if not self.project and self.pub_state == 'group':
            raise ValidationError(u"この素材はプロジェクトと結びついていないためプロジェクトメンバ限定公開に設定できません")
        if not self.title:
            self.title = self.file.name
        super(Material, self).clean()
        
    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        super(Material, self).save(request, *args, **kwargs)
        # 更新履歴登録
        if action is None:
            site.get_backend(Material).autodiscover(self, created)
    
    def modify_object_permission(self, mediator, created):
        # Permission
        # 著者には`manager`権限を与える
        mediator.manager(self, self.author, ['commons.view-pv_material'])
        if self.pub_state == 'public':
            # パブリックなものなので全員をviewerに
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        elif self.pub_state == 'protected':
            # 内部向けなので外部のみリジェクト
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'group':
            # グループ向けなのでそれ以外リジェクト
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
            mediator.viewer(self, self.project.group)
            
    @models.permalink
    def get_absolute_url(self):
        return ("commons-material-detail", (), {'object_id': self.pk})
    @models.permalink
    def get_download_url(self):
        return ("commons-material-download", (), {'object_id': self.pk})
    @models.permalink
    def get_preview_url(self):
        return ("commons-material-preview", (), {'object_id': self.pk,
            'filename': self.filename()})
    @models.permalink
    def get_thumbnail_url(self):
        return ("commons-material-thumbnail", (), {'object_id': self.pk})
    
    def filename(self):
        return os.path.basename(self.file.name)
    def filetype(self):
        return filetypes.guess(self.file.name)
    def mimetype(self):
        try:
            mimetypes.init()
            type = mimetypes.guess_type(self.file.name)[0]
        except:
            type = None
        return type
    def encoding(self):
        try:
            mimetypes.init()
            encoding = mimetypes.guess_type(self.file.name)[1]
        except:
            encoding = None
        return encoding
    
    def get_attache_tag(self):
        return "{commons: %d}" % self.pk
    
    def get_title_display(self):
        tag = u"""<a href="%(href)s" target="_blank">%(title)s</a><br /><small>添付タグ: %(tag)s</small>""" % {
            'href': self.get_absolute_url(),
            'title': self.title,
            'tag': self.get_attache_tag()
        }
        return mark_safe(tag)
    def get_download_link_display(self):
        return html._download_link(
            src=self.get_download_url(),
            src2=self.get_absolute_url(),
            file=self.file,
            mimetype=self.mimetype(),
            license=self.license)
    def get_thumbnail_display(self):
        return html.thumbnail_html(self, 320, 240)
    def get_digest_display(self):
        kwargs = {
            'src': reverse('commons-material-digest', kwargs={'object_id': self.pk}),
            'href': self.get_absolute_url(),
            'title': self.title,
            'alt': self.title,
        }
        html = u"""<a href="%(href)s" title="%(title)s"><img src="%(src)s" alt="%(alt)s" /></a>"""
        return mark_safe(html%kwargs)
