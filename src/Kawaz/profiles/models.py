# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from imagefield.fields import ImageField
from markitupfield.models import MarkItUpField
from defaultimg import get_default_profile_icon

from libwaz.contrib.googlemap.models import GoogleMapField
from libwaz.contrib.tagging.fields import TaggingField
from libwaz.contrib.object_permission import ObjectPermissionMediator

import os.path

class Skill(models.Model):
    u"""役職クラス"""
    label   = models.CharField(u"ラベル", unique=True, max_length=32)
    order   = models.IntegerField(u"並び順", default=0)
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        ordering            = ['order']
        verbose_name        = u"役職"
        verbose_name_plural = verbose_name

class ProfileManager(models.Manager):
    def published(self, request):
        qs = self.exclude(nickname=None).exclude(user__is_active=False)
        if request and request.user.is_authenticated():
            return qs
        else:
            return qs.filter(pub_state='public')

class Profile(models.Model):
    u"""プロフィールクラス"""
    def _get_upload_path(self, filename):
        path = u'storage/profiles/%s' % self.user.username
        return os.path.join(path, filename)
    
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
    )
    SEX_TYPES = (
        ('man',   u"男性"),
        ('woman', u"女性")
    )
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    # Required
    pub_state       = models.CharField(u"公開設定", max_length=10, choices=PUB_STATES, default="public")
    nickname        = models.CharField(u"ニックネーム", max_length=30, unique=True, blank=False, null=True)    # blank=False, null=Trueは必須設定
    # Non required
    mood            = models.CharField(u"ムードメッセージ", max_length=127, blank=True)
    icon            = ImageField(u"アイコン" , upload_to=_get_upload_path, blank=True, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS)
    sex             = models.CharField(u"性別", max_length=10, choices=SEX_TYPES, blank=True)
    birthday        = models.DateField(u"誕生日", null=True, blank=True)
    place           = models.CharField(u"居住地域", max_length=255, blank=True, help_text=u"居住地域は外部ユーザーには表示されません")
    location        = GoogleMapField(u"地図", blank=True, hidden=True, query_field_id='id__place', 
                                     help_text=u"あなたの住んでいる場所を登録することができます。登録しない場合は、"
                                               u"地図をしまって下さい。地図は外部ユーザーには表示されません")
    url             = models.URLField(u"URL", max_length=255, blank=True)
    remarks         = MarkItUpField(u"自由記入欄", default_markup_type='markdown', blank=True)
    skills          = models.ManyToManyField(Skill, verbose_name=u"役職", related_name='users', null=True, blank=True)
    # Uneditable
    user            = models.ForeignKey(User, verbose_name=u"アカウント", related_name='profile', unique=True, primary_key=True, editable=False)
    twitter_token   = models.CharField(u"Twitter oAuth Access Token", max_length=1023, editable=False, blank=True)
    created_at      = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at      = models.DateTimeField(u"更新日時", auto_now=True)
    
    tags            = TaggingField()
    
    objects         = ProfileManager()
    
    class Meta:
        ordering            = ('-user__last_login', 'nickname')
        verbose_name        = u"プロフィール"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return u"非アクティブユーザー: %s" % self.user.username
    
    def modify_object_permission(self, mediator, created):
        # Permission
        mediator.manager(self, self.user)
        if self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        else:
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')
            
    @models.permalink
    def get_absolute_url(self):
        return ("profiles-profile-detail", (), {'slug': self.user.username})
    
    def get_icon_display(self, pattern_name=None):
        kwargs = {
            'alt':      u"%sさんのアイコン"%self.nickname,
            'title':    u"%s 「%s」"%(self.nickname, self.mood),
        }
        if self.icon:
            kwargs['src'] = self.icon.url if not pattern_name else getattr(self.icon, pattern_name).url
        else:
            kwargs['src'] = get_default_profile_icon(pattern_name, self.pk)
        return mark_safe(u"""<img src="%(src)s" alt="%(alt)s" title="%(title)s" />""" % kwargs)
    get_icon_small_display = lambda self: self.get_icon_display('small')
    get_icon_middle_display = lambda self: self.get_icon_display('middle')
    get_icon_large_display = lambda self: self.get_icon_display('large')
    get_icon_huge_display = lambda self: self.get_icon_display('huge')
    
    def get_nickname_display(self):
        kwargs = {
            'href':   self.get_absolute_url(),
            'title':    u"@%s" % self.user.username,
            'nickname': self.nickname,
        }
        return mark_safe(u"""<a href="%(href)s" title="%(title)s">%(nickname)s</a>""" % kwargs)

    def is_authenticated_twitter(self):
        u"""twitter連携"""
        return bool(self.twitter_token)
    is_authenticated_twitter.short_description = u"Twitter連携"
    is_authenticated_twitter.boolean = True

class Service(models.Model):
    u"""ユーザーが使用しているサービス"""
    PUB_STATES = (
        settings.PUB_STATES['public'],
        settings.PUB_STATES['protected'],
    )
    SERVICES = (
        (u'skype',      u"Skype"),
        (u'wlm',        u"Windows Live Messenger"),
        (u'twitter',    u"Twitter"),
        (u'mixi',       u"mixi"),
        (u'facebook',   u"Facebook"),
        (u'foursquare', u"foursquare"),
        (u'google',     u"Google"),
        (u'pixiv',      u"Pixiv"),
        (u'hatena',     u"はてな"),
        (u'xbl',        u"Xbox Live"),
        (u'psn',        u"PlayStation Network"),
        (u'dropbox',    u"Dropbox"),
    )
    profile     = models.ForeignKey(Profile, verbose_name=u"プロフィール", related_name="services", editable=False)
    service     = models.CharField(u"サービス名", max_length=20, choices=SERVICES)
    account     = models.CharField(u"サービスアカウント", max_length=127)
    pub_state   = models.CharField(u"公開設定", max_length=10, choices=PUB_STATES, default="public")
    
    def get_account_display(self):
        SERVICE_LINKS = {
            "skype":       u"skype:%s?add",
            "wlm":         u"mailto:%s",
            "twitter":     u"http://twitter.com/%s/",
            "mixi":        u"http://mixi.jp/show_profile.pl?id=%s",
            "facebook":    u"http://www.facebook.com/%s",
            'foursquare':  u"http://foursquare.com/%s",
            "google":      u"mailto:%s@gmail.com",
            "pixiv":       u"http://www.pixiv.net/member.php?id=%s",
            "hatena":      u"http://d.hatena.ne.jp/%s/",
            "xbl":         u"http://live.xbox.com/ja-JP/MyXbox/Profile?gamertag=%s",
            "psn":         u"http://playstationhome.jp/community/mypage.php?OnlineID=%s",
            "dropbox":     u"mailto:%s",
        }
        return mark_safe(u"""<a href="%s" target="_blank">%s</a>""" % (
            SERVICE_LINKS[self.service] % self.account,
            self.account
        ))
        
    def get_service_icon_display(self):
        return mark_safe(u"""<img src="/image/serviceicons/%(service)s.png">""" %{'service':self.service})
    
    class Meta:
        verbose_name = u"サービス"
        verbose_name_plural = verbose_name
        # 同じサービスで同じアカウントの人は存在しないはず
        unique_together = ('service', 'account')
        
from django.db.models.signals import post_save
def create_profile(sender, instance, created, **kwargs):
    if created:
        #new = Profile(user=instance, nickname=instance.username)
        # nicknameが設定されているかどうかでユーザーが初回ログイン時に
        # プロフィールを更新したかどうかを判断するため自動では設定しない
        new = Profile(user=instance)
        new.save()
        # 自分のプロフィールなので管理者権限を与える
        ObjectPermissionMediator.manager(new, instance)
post_save.connect(create_profile, sender=User)
