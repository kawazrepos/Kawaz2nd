#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest of models.Profile


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
import datetime
from nose.tools import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import Profile

foo = None
profile = None

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
    # profile related should be created automatically
    if not Profile.objects.filter(user__username=username).exists():
        raise Exception(
                """Profile should be automatically created but none """
                """related profile is found.""")
    profile = user.profile
    # set nickname because nickname is required but not be created
    # automatically
    profile.nickname = username
    profile.full_clean()
    profile.save()
    return user, profile


def _delete_user(user):
    """delete user then related profile automatically removed"""
    _profile = user.profile
    # remove test user
    user.delete()
    # profile related should be removed automatically
    if Profile.objects.filter(pk=_profile.pk).exists():
        raise Exception(
                """Profile should be automatically deleted but """
                """related profile is found.""")


# this function should be appear at first of this module
def test_creation():
    """profile.Profile: creation works correctly"""
    global foo, profile
    foo, profile = _create_user()

def test_shortcut_property():
    """profile.Profile: User instance has shortcut property"""
    assert hasattr(User, 'profile'), 'User should have "profile" proeprty'
    global foo, profile
    foo, profile = _create_user()
    assert getattr(foo, 'profile') == profile, '"profile" property return wrong value'

def test_modification():
    """profile.Profile: modification works correctly"""
    kwargs = {
            'pub_state': 'protected',
            'nickname': 'foobar',
            'mood': 'foobar',
            'icon': '',
            'sex': 'man',
            'birthday': datetime.date(2000,1,1),
            'place': '',
            'location': '',
            'url': 'http://www.google.com',
            'remarks': 'foofoofoo',
            'twitter_token': '',
        }
    for key, value in kwargs.iteritems():
        setattr(profile, key, value)
    # call validation
    profile.full_clean()

    # check
    for key, value in kwargs.iteritems():
        eq_(getattr(profile, key), value)

    profile.save()

    found = Profile.objects.get(pk=profile.pk)
    # check
    for key, value in kwargs.iteritems():
        eq_(getattr(found, key), value)


def test_invalid_values():
    """profile.Profile: validation works correctly"""

    # pub_state should be in ['public', 'protected']
    profile.pub_state = 'foo'
    assert_raises(ValidationError, profile.full_clean)
    profile.pub_state = 'public'
    profile.full_clean()

    # nickname should not be empty
    profile.nickname = ''
    assert_raises(ValidationError, profile.full_clean)
    profile.nickname = 'foobar'
    profile.full_clean()

    # mood should has at most 127 characters
    profile.mood = '*' * 128
    assert_raises(ValidationError, profile.full_clean)
    profile.mood = ''
    profile.full_clean()

    # sex should be in ['man', 'woman']
    profile.sex = 'foo'
    assert_raises(ValidationError, profile.full_clean)
    profile.sex = ''
    profile.full_clean()
    
    # birthday should be an instance of datetime.date
    profile.birthday = 'foo'
    assert_raises(ValidationError, profile.full_clean)
    profile.birthday = None
    profile.full_clean()

    # url must be exist
    profile.url = 'foo'
    assert_raises(ValidationError, profile.full_clean)
    profile.url = ''
    profile.full_clean()


# This function should be appear at last of this module
def test_deletion():
    """profile.Profile: deletion works correctly"""
    _delete_user(foo)
