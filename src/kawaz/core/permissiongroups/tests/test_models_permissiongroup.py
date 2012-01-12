#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest of models.PermissionGroup


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
from nose.tools import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import PermissionGroup

foo = None
bar = None
hoge = None
normal_pgroup = None
staff_pgroup = None
promotable_pgroup = None
default_pgroup = None

def _create_user(username='foo'):
    """create user and return user and automatically generated profile"""
    # create test user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
                username=username,
                email='%s@test.com' % username,
                password=username)
    return user

def _clear_permission_cache(user):
    """clear cahced permissions in user"""
    if hasattr(user, '_perm_cache'):
        del user._perm_cache
    if hasattr(user, '_group_perm_cache'):
        del user._group_perm_cache

def setup():
    global foo, bar, hoge
    foo = _create_user(username='foo')
    bar = _create_user(username='bar')
    hoge = _create_user(username='hoge')

# this function should be appear at first of this module
def test_creation():
    """permissiongroups.PermissionGroup: creation works correctly"""
    global normal_pgroup, staff_pgroup, promotable_pgroup, default_pgroup
    normal_pgroup = PermissionGroup.objects.create_pgroup(
            codename='normal_pgroup',
            name='normal permission group',
            description='',
            permissions=[
                'permissiongroups.add_permissiongroup',
                'permissiongroups.change_permissiongroup',
                'permissiongroups.delete_permissiongroup'
            ])
    staff_pgroup = PermissionGroup.objects.create_pgroup(
            codename='staff_pgroup',
            name='staff permission group',
            description='',
            is_staff=True)
    promotable_pgroup = PermissionGroup.objects.create_pgroup(
            codename='promotable_pgroup',
            name='promotable permission group',
            description='',
            is_promotable=True)
    default_pgroup = PermissionGroup.objects.create_pgroup(
            codename='default_pgroup',
            name='default permission group',
            description='',
            is_default=True,
            permissions=[
                'auth.add_user',
                'auth.change_user',
                'auth.delete_user',
            ])

def test_adding_user():
    """permissiongroups.PermissionGroup: adding users works correctly"""
    normal_pgroup.add_users(foo)
    staff_pgroup.add_users(bar)
    promotable_pgroup.add_users(hoge)

    assert normal_pgroup.is_belong(foo)
    assert staff_pgroup.is_belong(bar)
    assert promotable_pgroup.is_belong(hoge)
    # User should belong to is_default=True permission groups
    assert default_pgroup.is_belong(foo)
    assert default_pgroup.is_belong(bar)
    assert default_pgroup.is_belong(hoge)
    # normal_group user should have permissions
    assert foo.has_perm('permissiongroups.add_permissiongroup')
    assert foo.has_perm('permissiongroups.change_permissiongroup')
    assert foo.has_perm('permissiongroups.delete_permissiongroup')

    # staff_group user should be is_staff=True
    assert bar.is_staff == True

    # promotable_group user should be is_promotable=True
    assert hoge.is_promotable == True

    # promote/demote can be executed only by promotable user
    assert_raises(AttributeError, foo.promote)
    assert_raises(AttributeError, foo.demote)
    assert_raises(AttributeError, bar.promote)
    assert_raises(AttributeError, bar.demote)
    hoge.promote()
    hoge.demote()

    # All user should have permissions
    assert foo.has_perm('auth.add_user')
    assert foo.has_perm('auth.change_user')
    assert foo.has_perm('auth.delete_user')
    assert bar.has_perm('auth.add_user')
    assert bar.has_perm('auth.change_user')
    assert bar.has_perm('auth.delete_user')
    assert hoge.has_perm('auth.add_user')
    assert hoge.has_perm('auth.change_user')
    assert hoge.has_perm('auth.delete_user')

def test_shortcut_properties_and_functions():
    """permissiongroups.PermissionGroup: User instance has shortcut properties and functions"""
    assert hasattr(User, 'is_promotable'), 'User should have "is_promotable" proeprty'
    assert hasattr(User, 'is_staff'), 'User should have "is_staff" proeprty'
    assert hasattr(User, 'promote'), 'User should have "promote" function'
    assert hasattr(User, 'demote'), 'User should have "demote" function'

def test_modification():
    """permissiongroups.PermissionGroup: modification works correctly"""
    assert foo.is_staff == False
    assert foo.is_promotable == False

    # is_staff
    normal_pgroup.is_staff = True
    normal_pgroup.save()
    assert foo.is_staff == True

    # is_promotable
    assert_raises(AttributeError, foo.promote)
    assert_raises(AttributeError, foo.demote)
    normal_pgroup.is_promotable = True
    normal_pgroup.save()
    assert foo.is_promotable == True
    assert foo.is_superuser == False
    foo.promote()
    assert foo.is_superuser == True
    foo.demote()
    assert foo.is_superuser == False

    # reset
    normal_pgroup.is_staff = False
    normal_pgroup.is_promotable = False
    normal_pgroup.save()

    # Adding permissions
    assert not foo.has_perm('auth.add_group')
    normal_pgroup.add_permissions('auth.add_group')
    _clear_permission_cache(foo)
    assert foo.has_perm('auth.add_group')

    # Removing permissions
    normal_pgroup.remove_permissions('auth.add_group')
    _clear_permission_cache(foo)
    assert not foo.has_perm('auth.add_group')

    # is_default
    assert not normal_pgroup.is_belong(bar)
    assert not normal_pgroup.is_belong(hoge)
    normal_pgroup.is_default=True
    normal_pgroup.save()
    assert normal_pgroup.is_belong(bar)
    assert normal_pgroup.is_belong(hoge)
    normal_pgroup.is_default=False
    normal_pgroup.save()
    normal_pgroup.remove_users([bar, hoge])
    assert not normal_pgroup.is_belong(bar)
    assert not normal_pgroup.is_belong(hoge)


def test_invalid_values():
    """permissiongroups.PermissionGroup: validation works correctly"""
    normal_pgroup.codename = None
    assert_raises(ValidationError, normal_pgroup.full_clean)

    normal_pgroup.codename = None
    assert_raises(ValidationError, normal_pgroup.full_clean)


# This function should be appear at last of this module
def test_deletion():
    """permissiongroups.PermissionGroup: deletion works correctly"""
    assert foo.has_perm('auth.add_user')

    default_pgroup.delete()

    assert not default_pgroup.is_belong(foo)
    assert not default_pgroup.is_belong(bar)
    assert not default_pgroup.is_belong(hoge)
    
    # django.contrib.auth.backend.ModelBackend use cache so clear it.
    _clear_permission_cache(foo)
    assert not foo.has_perm('auth.add_user')
