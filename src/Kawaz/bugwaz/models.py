# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/25
#
from django.conf import settings
from django.contrib.auth.models import User, Group

from libwaz.db import models
from libwaz.contrib.object_permission import ObjectPermissionMediator
from libwaz.contrib.history import site

class Component(models.Model):
    label       = models.CharField(u"ラベル", max_length=255)
    product     = models.ForeignKey('Product', related_name='components')
    class Meta:
        unique_together     = ('product', 'label')
        verbose_name        = u"コンポーネント"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.label
    @models.permalink
    def get_absolute_url(self):
        return ('bugwaz-component-detail', (), {'product': self.product.pk, 'object_id': self.pk})
    
    def delete(self):
        self.reports.clear()
        super(Component, self).delete()
        
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.product.group)
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
        
class Version(models.Model):
    label       = models.CharField(u"ラベル", max_length=255)
    product     = models.ForeignKey('Product', related_name='versions')
    class Meta:
        unique_together     = ('product', 'label')
        verbose_name        = u"バージョン"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.label
    @models.permalink
    def get_absolute_url(self):
        return ('bugwaz-version-detail', (), {'product': self.product.pk, 'object_id': self.pk})
    
    def delete(self):
        self.reports.clear()
        super(Version, self).delete()
        
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.product.group)
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
class Product(models.Model):
    label       = models.CharField(u"ラベル", max_length=255, unique=True)
    body        = models.TextField(u"本文", blank=True, help_text=u"プロダクト紹介文などに使用してください")
    rules       = models.TextField(u"レポート記載ルール", blank=True, help_text=u"バグ報告ページに表示されます")
    group       = models.ForeignKey(Group, verbose_name=u"開発者グループ")
    
    class Meta:
        verbose_name        = u"プロダクト"
        verbose_name_plural = verbose_name
        permissions = (
            ('add_component_product',   'Can add a component to the product'),
            ('add_version_product',     'Can add a version to the product'),
        )
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('bugwaz-product-detail', (), {'object_id': self.pk})
    
    @models.permalink
    def get_report_bug_url(self):
        return ('bugwaz-report-create', (), {'product': self.pk})
    
    def members(self):
        qs = User.objects.filter(is_active=True, groups=self.group)
        return qs
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.group, ['bugwaz.add_component_product', 'bugwaz.add_version_product'])
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
        
class Report(models.ModelWithRequest):
    STATUSES = (
        ('unconfirmed', u"未確認"),
        ('confirmed',   u"バグ確認済み"),
        ('readytofix',  u"バグ修正準備完了"),
        ('inprogress',  u"バグ修正中"),
        ('resolved',    u"修正完了"),
        ('verified',    u"修正確認済み")
    )
    RESOLUTIONS = (
        ('fixed',       u"修正済み"),
        ('invalid',     u"バグではない"),
        ('wontfix',     u"仕様なので修正しない"),
        ('later',       u"あとで修正する"),
        ('remind',      u"心に止めておく"),
        ('duplicate',   u"別に報告されたバグと同一"),
        ('worksforme',  u"バグ再現不可"),
        ('moved',       u"該当システムが扱うバグではない"),
        ('incomplete',  u"完全には修正できていない"),
        ('obsolete',    u"廃止された"),
    )
    SERVERITIES = (
        ('blocker',     u"このバグにより製品の実行が不可能"),
        ('critical',    u"このバグにより製品の重要機能が実行できない"),
        ('major',       u"このバグにより正常な動作を行わない"),
        ('normal',      u"直したほうがいいバグ"),
        ('minor',       u"そんなに重要ではないバグ"),
        ('trivial',     u"くだらないバグ"),
        ('enhancement', u"見た目に関係するバグ")
    )
    PRIORITIES = (
        ('1',           u"緊急"),
        ('2',           u"急いでやる"),
        ('3',           u"普通"),
        ('4',           u"そのうち"),
        ('5',           u"気が向いたら"),
    )
    OPERATING_SYSTEMS = (
        ('all',                 u"すべて"),
        ('win-xp',              u"Windows XP"),
        ('win-vista',           u"Windows Vista"),
        ('win-7',               u"Windows 7"),
        ('mac-tiger',           u"Mac OS X Tiger"),
        ('mac-leopard',         u"Mac OS X Leopard"),
        ('mac-snow-leopard',    u"Mac OS X Snow Leopard"),
        ('ubuntu-1004',         u"Ubuntu 10.04"),
        ('ubuntu-1010',         u"Ubuntu 10.10"),
        ('linux',               u"Linux"),
        ('freebsd',             u"Free BSD"),
        ('solaris',             u"Solaris"),
        ('other',               u"その他")
    )
    # Required
    product     = models.ForeignKey(Product, verbose_name=u"対象プロダクト", related_name='reports')
    label       = models.CharField(u"ラベル", max_length=120, help_text=u"バグのラベルです。バグ内容の要約を記載してください")
    body        = models.TextField(u"バグ内容", help_text=u"バグの内容です。バグの再現ができるようにバグに至ったまでにとった行動すべてを記載してください")
    username    = models.CharField(u"報告者名", max_length=120)
    # Omittable
    component   = models.ForeignKey(Component, verbose_name=u"対象コンポーネント", related_name='reports', blank=True, null=True)
    version     = models.ForeignKey(Version, verbose_name=u"対象バージョン", related_name='reports', blank=True, null=True)
    serverity   = models.CharField(u"深刻度", max_length=20, choices=SERVERITIES, blank=True)
    os          = models.CharField(u"使用しているOS", max_length=20, choices=OPERATING_SYSTEMS, blank=True)
    # Uneditable
    status      = models.CharField(u"ステータス", max_length=20, choices=STATUSES, default='unconfirmed')
    resolution  = models.CharField(u"処理方法", max_length=20, choices=RESOLUTIONS, blank=True, default='')
    priority    = models.CharField(u"優先度", max_length=20, choices=PRIORITIES, blank=True, default='')
    charges     = models.ManyToManyField(User, verbose_name=u"担当者", related_name='reports_charged')
    author      = models.ForeignKey(User, verbose_name=u"作成者", related_name='reports_created', null=True, editable=False)
    ip_address  = models.IPAddressField(u"IP Address", editable=False, null=True)
    created_at  = models.DateTimeField(u"作成日時", auto_now_add=True)
    updated_at  = models.DateTimeField(u"更新日時", auto_now=True)
    
    class Meta:
        ordering            = ('status', 'priority', 'product', '-updated_at')
        unique_together     = ('product', 'label')
        verbose_name        = u"レポート"
        verbose_name_plural = verbose_name
        permissions = (
            ('charge_report',   'Can charge the report'),
            ('status_report',   'Can change a status of the report'),
        )
    def __unicode__(self):
        return u"%s - %s" % (self.label, self.product)
    
    @models.permalink
    def get_absolute_url(self):
        return ('bugwaz-report-detail', (), {'product': self.product.pk, 'object_id': self.pk})

    def save(self, request=None, action=None, *args, **kwargs):
        created = self.pk is None
        if self.pk is None and request and request.user.is_authenticated():
            self.author = request.user
        if self.pk is None and request:
            self.ip_address = request.META['REMOTE_ADDR']
        super(Report, self).save(request, *args, **kwargs)
        if action is None:
            site.get_backend(Report).autodiscover(self, created)
        elif action == 'charge':
            if self.charges.count() == 1:
                site.get_backend(Report).autodiscover(self, 'charge')
        elif action == 'discharge':
            if self.charges.count() == 0:
                site.get_backend(Report).autodiscover(self, 'discharge')
        else:
            site.get_backend(Report).autodiscover(self, action)
            
    def join(self, user):
        self.charges.add(user)
        self.save(action='charge')
            
    def quit(self, user):
        self.charges.remove(user)
        self.save(action='discharge')
        
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author, [] if not self.author in self.charges.all() else ['bugwaz.status_report'])
        mediator.viewer(self, self.product.group, ['bugwaz.charge_report'])
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
    
    def modify_object_permission_m2m(self, mediator, sender, model, pk_set, removed):
        if sender == self.charges.through:
            for charge in model.objects.filter(pk__in=pk_set):
                if not removed:
                    mediator.viewer(self, charge, ['bugwaz.status_report'])
                else:
                    mediator.discontribute(self, charge, ['bugwaz.status_report'])