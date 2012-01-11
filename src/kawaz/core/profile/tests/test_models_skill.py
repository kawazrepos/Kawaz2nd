#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of models.Skill


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
from django.core.exceptions import ValidationError

from test_models_profile import _create_user
from test_models_profile import _delete_user
from ..models import Skill

foo = None
profile = None
skill = None

def setup():
    """setup function"""
    global foo, profile
    # create user, profile
    foo, profile = _create_user()


def teardown():
    """teardown function"""
    # delete user, profile
    _delete_user(foo)

def test_creation():
    """profile.Skill: creation works correctly"""
    global skill
    skill = Skill(label='foo')
    skill.full_clean()
    skill.save()

def test_modification():
    """profile.Skill: modification works correctly"""
    skill.label = 'bar'
    skill.full_clean()
    skill.save()

def test_adding_to_profile():
    """profile.Skill: adding to profile works correctly"""
    profile.skills.add(skill)
    ok_(profile.skills.filter(pk=skill.pk).exists())

def test_removing_from_profile():
    """profile.Skill: removing from profile works correctly"""
    profile.skills.remove(skill)
    ok_(not profile.skills.filter(pk=skill.pk).exists())

def test_invalid_values():
    """profile.Skill: validation works correctly"""
    
    # label should at most 32 characters
    skill.label = '*' * 33
    assert_raises(ValidationError, skill.full_clean)
    skill.label = 'foo'
    skill.full_clean()

    # TODO: label should be unique


def test_deletion():
    """profile.Skill: deletion works correctly"""
    skill.delete()
            
