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
from django.core.exceptions import ValidationError

from test_models_profile import BaseTestCase
from ..models import Service

class ProfilesServiceModelTestCase(BaseTestCase):
    """Test collection for profiles.Service"""

    def setUp(self):
        self.foo = self._create_user('foo')
        self.profile = self.foo.profile

    def test_creation(self):
        """profile.Service: creation works correctly"""
        global service
        service = Service(
                profile=self.profile,
                pub_state='public',
                service='skype',
                account='foobar')
        service.full_clean()
        service.save()

        return service


    def test_modification(self):
        """profile.Service: modification works correctly"""
        service = self.test_creation()

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
            self.assertEqual(getattr(service, key), value)

        service.save()

        found = Service.objects.get(pk=service.pk)
        # check
        for key, value in kwargs.iteritems():
            self.assertEqual(getattr(found, key), value)


    def test_invalid_values(self):
        """profile.Service: validation works correctly"""
        service = self.test_creation()

        # pub_state should be in ['public', 'protected']
        service.pub_state = 'foo'
        self.assertRaises(ValidationError, service.full_clean)
        service.pub_state = 'public'
        service.full_clean()

        # service should be in one of Service.SERVICES
        service.service = 'foo'
        self.assertRaises(ValidationError, service.full_clean)
        service.service = 'skype'
        service.full_clean()

        # account should at most 127 characters
        service.account = '*' * 128
        self.assertRaises(ValidationError, service.full_clean)
        service.account = 'foo'
        service.full_clean()

        # TODO: validate `unique_together`

    def test_deletion(self):
        """profile.Service: deletion works correctly"""
        # create new user, profile, service
        new_user = self._create_user('bar')
        new_profile = new_user.profile
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
