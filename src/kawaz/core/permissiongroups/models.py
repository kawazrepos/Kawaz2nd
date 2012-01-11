#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
PermissionGroup models


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.text import ugettext_lazy as _


class PermissionGroupManager(models.Manager):
    """Manager of PermissionGroup
    
    Attribute:
        get_by_natural_key - get permission group by natural key
    
    >>> manager = PermissionGroupManager()
    >>> assert hasattr(manager, 'get_by_natural_key')
    """
    def get_by_natural_key(self, codename):
        """return permissiongroup by natural key"""
        return self.get(codename=codename)

    def get_by_user(self, user):
        """return permission groups by user"""
        return self.filter(group__in=user.groups)
    
class PermissionGroup(models.Model):
    """PermissionGroup model
    
    Attribute:
        codename - A code name of the permission group 
        name - A name of permission group
        description - A description of permission group
        group - Group used for adding permissions to permission group
        is_staff - User belongs to is staff
        is_promotable - User belongs to can promote to superuser
        is_default - Newly created user belongs to this permission group

        users - Users belongs to this permission group
        permissions - Permissions belongs to this permission group

        natural_key - return natural key (currently codename)

    >>> pgroup = PermissionGroup()

    # Attributes profile should have
    >>> assert hasattr(pgroup, 'codename')
    >>> assert hasattr(pgroup, 'name')
    >>> assert hasattr(pgroup, 'description')
    >>> assert hasattr(pgroup, 'group')
    >>> assert hasattr(pgroup, 'is_staff')
    >>> assert hasattr(pgroup, 'is_promotable')
    >>> assert hasattr(pgroup, 'is_default')

    # Required properties
    >>> assert hasattr(pgroup, 'users')
    >>> assert hasattr(pgroup, 'permissions')

    # Required functions
    >>> assert hasattr(pgroup, 'natural_key')
    """
    codename = models.SlugField(
            _('code name'), max_length=255, unique=True,
            help_text=_('A codename of PermissionGroup. Used as group name when group name is omitted.'))
    name = models.CharField(
            _('name'), max_length=255, 
            help_text=_('A name of PermissionGroup. Used in list'))
    description = models.TextField(
            _('description'),
            help_text=_('A description of PermissionGroup. Notice that HTML is allowed'))
    group = models.ForeignKey(
            Group, verbose_name=_('Target group'), editable=False, unique=True,
            help_text=_('Used for adding permission. codename is used as name of group when is omitted.'))
    is_staff = models.BooleanField(
            _('is staff'), default=False, 
            help_text=_('user belongs to is staff'))
    is_promotable = models.BooleanField(
            _('is promotable'), default=False, 
            help_text=_('User belongs to can promote to superuser'))
    is_default = models.BooleanField(
            _('is default'), default=False,
            help_text=_('newly created user belongs to this permission group'))
    
    objects = PermissionGroupManager()
    
    @models.permalink
    def get_absolute_url(self):
        return (r'permissiongroups-permissiongroup-detail', (), {'object_id': self.pk})
    
    def clean(self):
        if not hasattr(self, 'group') or self.group is None:
            self.group = Group.objects.get_or_create(name=self.codename)[0]
        super(PermissionGroup, self).clean()
    
    @property
    def users(self):
        """return users belongs to this permission group"""
        return self.group.user_set

    @property
    def permissions(self):
        """return permissions belongs to this permission group"""
        return self.group.permissions
    
    def natural_key(self):
        """get natural key of this permission"""
        return self.codename
#
# Add extra properties to django.contrib.auth.models.User
# 
# Warning:
#   Default 'is_staff' is overwrited by 'is_staff' property
#
def is_promotable(self):
    """return whether the user can promote to superuser"""
    qs = PermissionGroup.objects.get_by_user(self)
    for pgroup in qs:
        if pgroup.is_promotable:
            return True
    return False
def is_staff(self):
    """return whether the user is staff"""
    qs = PermissionGroup.objects.get_by_user(self)
    for pgroup in qs:
        if pgroup.is_staff:
            return True
    return False
User.is_promotable = property(is_promotable)
User.is_staff = property(is_staff)

#
# Belong newly created user to default permission group
#
from django.db.models import signals
def post_save_callback(sender, instance, created, **kwargs):
    if created:
        permission_groups = PermissionGroup.objects.filter(is_default=True)
        for permission_group in permission_groups:
            permission_group.users.add(instance)
        instance.save()
signals.post_save.connect(post_save_callback, sender=User)
