# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django.db import models
from django.contrib.auth.models import User, Group


class PermissionGroupManager(models.Manager):
    def get_by_natural_key(self, codename):
        return self.get(codename=codename)
    
class PermissionGroup(models.Model):
    codename        = models.SlugField(u"コードネーム", max_length=255, unique=True,
                                       help_text=u"使用されるコードネームです。対象グループを省略した場合にグループ名として利用されます")
    name            = models.CharField(u"名前", max_length=255, 
                                       help_text=u"パーミッショングループ一覧で表示される名称です")
    description     = models.TextField(u"説明", 
                                       help_text=u"パーミッショングループの説明です。HTMLが許可されているので注意してください")
    group           = models.ForeignKey(Group, verbose_name="対象グループ", editable=False, unique=True,
                                        help_text=u"パーミッション付加などで使用される`auth.group`です。省略時はコードネームがそのまま使用されます")
    is_staff        = models.BooleanField(u"スタッフグループ", default=False, 
                                          help_text=u"このグループに属するユーザーをスタッフユーザーにする")
    is_promotable   = models.BooleanField(u"昇格可能グループ", default=False, 
                                          help_text=u"このグループに属するユーザーをスーパーユーザに昇格可能にする")
    is_default      = models.BooleanField(u"デフォルトグループ", default=False,
                                          help_text=u"新規作成ユーザーを自動的にこのグループに所属させます")
    
    objects         = PermissionGroupManager()
    
    @models.permalink
    def get_absolute_url(self):
        return (r'permissiongroups-permissiongroup-detail', (), {'object_id': self.pk})
    
    def clean(self):
        if not hasattr(self, 'group') or self.group is None:
            self.group = Group.objects.get_or_create(name=self.codename)[0]
        super(PermissionGroup, self).clean()
    
    @property
    def users(self):
        return self.group.user_set
    @property
    def permissions(self):
        return self.group.permissions
    
    def save(self, *args, **kwargs):
        super(PermissionGroup, self).save(*args, **kwargs)
        # 以下必要か微妙
        #self.group.save()
        
    def natural_key(self):
        return self.codename
#
# 新規ユーザー作成時に自動的にデフォルトパーミッショングループに参加させる
#
from django.db.models import signals
def post_save_callback(sender, instance, created, **kwargs):
    if created:
        permission_groups = PermissionGroup.objects.filter(is_default=True)
        for permission_group in permission_groups:
            permission_group.users.add(instance)
        instance.save()
signals.post_save.connect(post_save_callback, sender=User)