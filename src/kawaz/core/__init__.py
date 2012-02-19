#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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
from django.contrib.auth.models import Group
from permissiongroups.models import PermissionGroup

def get_or_create_permissiongroup(codename):
    """get or create permissiongroup"""
    try:
        pgroup = PermissionGroup.objects.get(codename=codename)
        return pgroup
    except PermissionGroup.DoesNotExist:
        kwargs = {
                'codename': codename,
                'name': codename.capitalize(),
                'group': Group.objects.get_or_create(name='permissiongroup-%s'%codename)[0]
            }
        if codename == 'zeele':
            kwargs2 = {
                    'is_staff': True,
                    'is_promotable': True,
                }
            permissions = (
                    'auth.add_user',
                    'auth.change_user',
                    'auth.delete_user',
                    'auth.add_group',
                    'auth.change_group',
                    'auth.delete_group',
                    'auth.add_permission',
                    'auth.change_permission',
                    'auth.delete_permission',
                    'permissiongroups.add_permissiongroup',
                    'permissiongroups.change_permissiongroup',
                    'permissiongroups.delete_permissiongroup',
                )
        elif codename == 'nerv':
            kwargs2 = {
                    'is_staff': True,
                    'is_promotable': False,
                }
            permissions = tuple()
        elif codename == 'children':
            kwargs2 = {
                    'is_staff': False,
                    'is_promotable': False,
                }
            permissions = tuple()
        elif codename == 'visitor':
            kwargs2 = {
                    'is_staff': False,
                    'is_promotable': False,
                }
            permissions = tuple()
        else:
            raise AttributeError('Unknown permissiongroup codename (%s) is passed.' % codename)
        kwargs.update(kwargs2)
        pgroup = PermissionGroup.objects.create(**kwargs)
        pgroup.add_permissions(permissions)
        return pgroup

def get_zeele_pgroup():
    """get zeele permissiongroup"""
    return get_or_create_permissiongroup(codename='zeele')

def get_nerv_pgroup():
    """get nerv permissiongroup"""
    return get_or_create_permissiongroup(codename='nerv')

def get_children_pgroup():
    """get children permissiongroup"""
    return get_or_create_permissiongroup(codename='children')

def get_visitor_pgroup():
    """get visitor permissiongroup"""
    return get_or_create_permissiongroup(codename='visitor')

def get_permissiongroup_group(pgroup):
    """get group of permissiongroup"""
    return pgroup.group

def get_zeele_group():
    """get zeele permissiongroup group"""
    pgroup = get_zeele_pgroup()
    return get_permissiongroup_group(pgroup)

def get_nerv_group():
    """get nerv permissiongroup group"""
    pgroup = get_nerv_pgroup()
    return get_permissiongroup_group(pgroup)

def get_children_group():
    """get children permissiongroup group"""
    pgroup = get_children_pgroup()
    return get_permissiongroup_group(pgroup)

def get_visitor_group():
    """get visitor permissiongroup group"""
    pgroup = get_visitor_pgroup()
    return get_permissiongroup_group(pgroup)
