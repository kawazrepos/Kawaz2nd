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
from django.contrib.auth.models import Permission
from django.utils.text import ugettext_lazy as _


from kawaz.utils.uuid import uuid1, uuid3

import logging
logger = logging.getLogger(__name__)

# Create NAMESPACE UUID for create unique group name
NAMESPACE_CN = uuid1()

def isiteratable(obj):
    if hasattr(obj, '__iter__') and hasattr(obj, 'next'):
        return True
    elif isinstance(obj, (list, tuple)):
        return True
    return False
class PermissionGroupManager(models.Manager):
    """Manager of PermissionGroup
    
    Attribute:
        get_by_natural_key - get permission group by natural key
        get_by_user - get permissino groups by user
        create_pgroup - create permission group
    
    >>> manager = PermissionGroupManager()
    >>> assert hasattr(manager, 'get_by_natural_key')
    >>> assert hasattr(manager, 'get_by_user')
    >>> assert hasattr(manager, 'create_pgroup')
    """
    def get_by_natural_key(self, codename):
        """return permissiongroup by natural key"""
        return self.get(codename=codename)

    def get_by_user(self, user):
        """return permission groups by user"""
        return self.filter(group__in=user.groups.iterator())

    def create_pgroup(self, codename, name, description, group=None,
                      is_staff=False, is_promotable=False, is_default=False,
                      permissions=None):
        """create permission group"""
        pgroup = self.create(
                codename=codename, name=name, description=description, group=group,
                is_staff=is_staff, is_promotable=is_promotable, is_default=is_default)
        if permissions:
            pgroup.add_permissions(permissions)
        return pgroup

    
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
        add_users - add users to this permission group
        remove_users - remove users from this permission group
        add_permissions - add permissions to this permission group
        remove_permissions - remove permissions from this permission group

    >>> pgroup = PermissionGroup(codename='test_perission_group')
    >>> pgroup.save()   # this is required to set 'group'

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
    >>> assert hasattr(pgroup, 'add_users')
    >>> assert hasattr(pgroup, 'remove_users')
    >>> assert hasattr(pgroup, 'add_permissions')
    >>> assert hasattr(pgroup, 'remove_permissions')
    """
    codename = models.SlugField(
            _('code name'), max_length=255, unique=True,
            help_text=_('A codename of PermissionGroup. Used as seed for creating unique group name when group is omitted.'))
    name = models.CharField(
            _('name'), max_length=255, 
            help_text=_('A name of PermissionGroup. Used in list'))
    description = models.TextField(
            _('description'),
            help_text=_('A description of PermissionGroup. Notice that HTML is allowed'))
    group = models.ForeignKey(
            Group, verbose_name=_('Target group'), unique=True, default=None, null=True,
            help_text=_('Used for adding permission. codename is used as seed for creating unique group name when is omitted.'))
    is_staff = models.BooleanField(
            _('is staff'), default=False, 
            help_text=_('User belongs to is staff'))
    is_promotable = models.BooleanField(
            _('is promotable'), default=False, 
            help_text=_('User belongs to can promote to superuser'))
    is_default = models.BooleanField(
            _('is default'), default=False,
            help_text=_('Newly created user belongs to this permission group'))
    
    objects = PermissionGroupManager()
    
    @models.permalink
    def get_absolute_url(self):
        return (r'permissiongroups-permissiongroup-detail', (), {'object_id': self.pk})
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'group') or self.group is None:
            def create_unique_group_name(codename):
                """create unique group name via GUID"""
                # Note: group name must be lower than 80 characters
                guid = uuid3(NAMESPACE_CN, codename)
                return "permissiongroup-%s" % str(guid)
            group_name = create_unique_group_name(self.codename)
            group = Group.objects.create(name=group_name)
            logger.debug('"group" is not specified thus "%s" group is newly created.' % group_name)
            self.group = group
        super(PermissionGroup, self).save(*args, **kwargs)
        if self.is_default:
            # Join all exists users to this permission group
            self.add_users(User.objects.iterator())

    def delete(self, *args, **kwargs):
        # Delete group as well
        self.group.delete()
        super(PermissionGroup, self).delete(*args, **kwargs)
    
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

    def is_belong(self, user):
        """is the user belongs to this permission group"""
        if self.pk is None:
            return False
        return user in self.users.all()

    def add_users(self, users):
        """add users to this permission group"""
        if isinstance(users, User):
            users = [users]
        elif not isiteratable(users):
            raise AttributeError('"users" must be iteratable')
        for user in users:
            self.users.add(user)

    def remove_users(self, users):
        """remove users from this permission group"""
        if isinstance(users, User):
            users = [users]
        elif not isiteratable(users):
            raise AttributeError('"users" must be iteratable')
        for user in users:
            self.users.remove(user)

    def _get_permission_instance(self, permission):
        """get permission instance from an instance or natural_key"""
        if isinstance(permission, basestring):
            # get permission by natural key
            try:
                app_label, codename = permission.split('.', 1)
            except IndexError:
                raise AttributeError('"permission" must be "app_label.codename_model". given "%s"' % permission)
            try:
                model = codename.rsplit('_', 1)[1]
            except IndexError:
                raise AttributeError('"permission" must be "app_label.codename_model". given "%s"' % permission)
            try:
                perm = Permission.objects.get_by_natural_key(codename, app_label, model)
            except Permission.DoesNotExist:
                raise AttributeError('permission "%s" does not exist' % permission)
        elif isinstance(permission, Permission):
            # permission is already an instance of Permissions
            perm = permission
        else:
            raise AttributeError('"permission" must be an instance or natural_key of Permission')
        return perm

    def add_permissions(self, permissions):
        """add permissins to this permission group"""
        if isinstance(permissions, (basestring, Permission)):
            permissions = [permissions]
        elif not isiteratable(permissions):
            raise AttributeError('"permissions" must be iteratable')
        for permission in permissions:
            perm = self._get_permission_instance(permission)
            self.permissions.add(perm)

    def remove_permissions(self, permissions):
        """remove permissins from this permission group"""
        if isinstance(permissions, (basestring, Permission)):
            permissions = [permissions]
        elif not isiteratable(permissions):
            raise AttributeError('"permissions" must be iteratable')
        for permission in permissions:
            perm = self._get_permission_instance(permission)
            self.permissions.remove(perm)

#
# Add extra properties/functions to django.contrib.auth.models.User
# 
# Warning:
#   Default 'is_staff' is overwrited by 'is_staff' property
#
def is_promotable(self):
    """return whether the user can promote to superuser"""
    if self.pk is None:
        return False
    qs = PermissionGroup.objects.get_by_user(self)
    for pgroup in qs:
        if pgroup.is_promotable:
            return True
    return False
def is_staff(self):
    """return whether the user is staff"""
    if self.pk is None:
        return False
    qs = PermissionGroup.objects.get_by_user(self)
    for pgroup in qs:
        if pgroup.is_staff:
            return True
    return False
def promote(self):
    """promote user to superuser"""
    if self.is_promotable:
        self.is_superuser = True
        self.save()
    else:
        raise AttributeError('"is_promotable" must be True for promoting')
def demote(self):
    """demote user from superuser"""
    if self.is_promotable:
        self.is_superuser = False
        self.save()
    else:
        raise AttributeError('"is_promotable" must be True for demoting')
User.is_promotable = property(is_promotable)
User.is_staff = property(is_staff, lambda self, value: None) # set dummy setter
User.promote = promote
User.demote = demote

#
# Belong newly created user to default permission group
#
from django.db.models import signals
def post_save_callback(sender, instance, created, **kwargs):
    if created:
        permission_groups = PermissionGroup.objects.filter(is_default=True)
        for permission_group in permission_groups:
            permission_group.users.add(instance)
        logger.debug('Newly created user belong to %d permission group(s)' % permission_groups.count())
        instance.save()
signals.post_save.connect(post_save_callback, sender=User)
