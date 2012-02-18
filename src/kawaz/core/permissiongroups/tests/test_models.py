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
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import PermissionGroup

class PermissionGroupModelTestCase(TestCase):
    def _create_user(self, username):
        kwargs = {
                'username': username,
                'email': '%s@test.com' % username,
                'password': 'password',
            }
        return User.objects.create_user(**kwargs)

    def _clear_permission_cache(self, user):
        if hasattr(user, '_perm_cache'):
            del user._perm_cache
        if hasattr(user, '_group_perm_cache'):
            del user._group_perm_cache

    def setUp(self):
        self.foo = self._create_user('foo')
        self.bar = self._create_user('bar')
        self.hoge = self._create_user('hoge')

    def test_creation(self):
        """permissiongroups.PermissionGroup: creation works correctly"""
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
        return normal_pgroup, staff_pgroup, promotable_pgroup

    def test_adding_user(self):
        """permissiongroups.PermissionGroup: adding users works correctly"""
        normal_pgroup, staff_pgroup, promotable_pgroup = self.test_creation()

        normal_pgroup.add_users(self.foo)
        staff_pgroup.add_users(self.bar)
        promotable_pgroup.add_users(self.hoge)

        assert normal_pgroup.is_belong(self.foo)
        assert staff_pgroup.is_belong(self.bar)
        assert promotable_pgroup.is_belong(self.hoge)
        # normal_group user should have permissions
        assert self.foo.has_perm('permissiongroups.add_permissiongroup')
        assert self.foo.has_perm('permissiongroups.change_permissiongroup')
        assert self.foo.has_perm('permissiongroups.delete_permissiongroup')

        # staff_group user should be is_staff=True
        assert self.bar.is_staff == True

        # promotable_group user should be is_promotable=True
        assert self.hoge.is_promotable == True

        # promote/demote can be executed only by promotable user
        self.assertRaises(AttributeError, self.foo.promote)
        self.assertRaises(AttributeError, self.foo.demote)
        self.assertRaises(AttributeError, self.bar.promote)
        self.assertRaises(AttributeError, self.bar.demote)
        self.hoge.promote()
        self.hoge.demote()

    def test_shortcut_properties_and_functions(self):
        """permissiongroups.PermissionGroup: User instance has shortcut properties and functions"""
        assert hasattr(User, 'is_promotable'), 'User should have "is_promotable" proeprty'
        assert hasattr(User, 'is_staff'), 'User should have "is_staff" proeprty'
        assert hasattr(User, 'promote'), 'User should have "promote" function'
        assert hasattr(User, 'demote'), 'User should have "demote" function'

    def test_modification(self):
        """permissiongroups.PermissionGroup: modification works correctly"""
        normal_pgroup, staff_pgroup, promotable_pgroup = self.test_creation()

        normal_pgroup.add_users(self.foo)
        staff_pgroup.add_users(self.bar)
        promotable_pgroup.add_users(self.hoge)

        assert self.foo.is_staff == False
        assert self.foo.is_promotable == False

        # is_staff
        normal_pgroup.is_staff = True
        normal_pgroup.save()
        #self.foo = User.objects.get(username='foo')
        assert self.foo.is_staff == True

        # is_promotable
        self.assertRaises(AttributeError, self.foo.promote)
        self.assertRaises(AttributeError, self.foo.demote)
        normal_pgroup.is_promotable = True
        normal_pgroup.save()
        assert self.foo.is_promotable == True
        assert self.foo.is_superuser == False
        self.foo.promote()
        assert self.foo.is_superuser == True
        self.foo.demote()
        assert self.foo.is_superuser == False

        # reset
        normal_pgroup.is_staff = False
        normal_pgroup.is_promotable = False
        normal_pgroup.save()

        # Adding permissions
        assert not self.foo.has_perm('auth.add_group')
        normal_pgroup.add_permissions('auth.add_group')
        self._clear_permission_cache(self.foo)
        assert self.foo.has_perm('auth.add_group')

        # Removing permissions
        normal_pgroup.remove_permissions('auth.add_group')
        self._clear_permission_cache(self.foo)
        assert not self.foo.has_perm('auth.add_group')


    def test_invalid_values(self):
        """permissiongroups.PermissionGroup: validation works correctly"""
        normal_pgroup, staff_pgroup, promotable_pgroup = self.test_creation()

        normal_pgroup.codename = None
        self.assertRaises(ValidationError, normal_pgroup.full_clean)

        normal_pgroup.codename = None
        self.assertRaises(ValidationError, normal_pgroup.full_clean)


    def test_deletion(self):
        """permissiongroups.PermissionGroup: deletion works correctly"""
        normal_pgroup, staff_pgroup, promotable_pgroup = self.test_creation()

        normal_pgroup.add_users(self.foo)
        normal_pgroup.add_users(self.bar)
        normal_pgroup.add_users(self.hoge)
        assert self.foo.has_perm('permissiongroups.add_permissiongroup')

        normal_pgroup.delete()

        assert not normal_pgroup.is_belong(self.foo)
        assert not normal_pgroup.is_belong(self.bar)
        assert not normal_pgroup.is_belong(self.hoge)
        
        # django.contrib.auth.backend.ModelBackend use cache so clear it.
        self._clear_permission_cache(self.foo)
        assert not self.foo.has_perm('permissiongroups.add_permissiongroup')
