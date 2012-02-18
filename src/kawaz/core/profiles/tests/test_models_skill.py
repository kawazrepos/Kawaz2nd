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
from django.core.exceptions import ValidationError

from test_models_profile import BaseTestCase
from ..models import Skill

class ProfilesSkillModelTestCase(BaseTestCase):
    """Test collection for profiles.Skill"""
    def setUp(self):
        self.foo = self._create_user('foo')
        self.profile = self.foo.profile

    def test_creation(self):
        """profile.Skill: creation works correctly"""
        skill = Skill(label='foo')
        skill.full_clean()
        skill.save()

        return skill

    def test_modification(self):
        """profile.Skill: modification works correctly"""
        skill = self.test_creation()

        skill.label = 'bar'
        skill.full_clean()
        skill.save()

    def test_adding_to_profile(self):
        """profile.Skill: adding to profile works correctly"""
        skill = self.test_creation()

        self.profile.skills.add(skill)
        assert self.profile.skills.filter(pk=skill.pk).exists()

    def test_removing_from_profile(self):
        """profile.Skill: removing from profile works correctly"""
        skill = self.test_creation()

        self.profile.skills.remove(skill)
        assert not self.profile.skills.filter(pk=skill.pk).exists()

    def test_invalid_values(self):
        """profile.Skill: validation works correctly"""
        skill = self.test_creation()
        
        # label should at most 32 characters
        skill.label = '*' * 33
        self.assertRaises(ValidationError, skill.full_clean)
        skill.label = 'foo'
        skill.full_clean()

        # TODO: label should be unique


    def test_deletion(self):
        """profile.Skill: deletion works correctly"""
        skill = self.test_creation()

        skill.delete()
                
