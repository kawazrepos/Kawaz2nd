#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of models.Service


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
from ..models import Service

foo = None
profile = None
service = None

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
    """profile.Service: creation works correctly"""
    global service
    service = Service(
            profile=profile,
            pub_state='public',
            service='skype',
            account='foobar')
    service.full_clean()
    service.save()


def test_modification():
    """profile.Service: modification works correctly"""
    kwargs = {
            'pub_state': 'protected',
            'service': 'twitter',
            'account': 'hogehoge',
        }
    for key, value in kwargs.iteritems():
        setattr(service, key, value)
    # call validation
    service.full_clean()

    # check
    for key, value in kwargs.iteritems():
        eq_(getattr(service, key), value)

    service.save()

    found = Service.objects.get(pk=service.pk)
    # check
    for key, value in kwargs.iteritems():
        eq_(getattr(found, key), value)


def test_invalid_values():
    """profile.Service: validation works correctly"""

    # pub_state should be in ['public', 'protected']
    service.pub_state = 'foo'
    assert_raises(ValidationError, service.full_clean)
    service.pub_state = 'public'
    service.full_clean()

    # service should be in one of Service.SERVICES
    service.service = 'foo'
    assert_raises(ValidationError, service.full_clean)
    service.service = 'skype'
    service.full_clean()

    # account should at most 127 characters
    service.account = '*' * 128
    assert_raises(ValidationError, service.full_clean)
    service.account = 'foo'
    service.full_clean()

    # TODO: validate `unique_together`

def test_deletion():
    """profile.Service: deletion works correctly"""
    service.delete()

    # create new user, profile, service
    new_user, new_profile = _create_user('bar')
    new_service = Service.objects.create(
            profile=new_profile,
            service='skype',
            account='bar')

    # delete user will delete service as well
    new_user.delete()
    if Service.objects.filter(pk=new_service.pk).exists():
        raise Exception(
                """Service should be automatically deleted but related """
                """service is found.""")
