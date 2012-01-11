#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
django-filter filterset collection for profile application


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
from django.utils.text import ugettext_lazy as _

from django_filters import filters
from django_filters import filterset
from django_filters import widgets
from universaltag.filters import UniversalTagFilter

from models import Skill
from models import Profile

class ProfileFilterSet(filterset.FilterSet):
    """filterset of profile application"""
    skills = filters.ModelChoiceFilter(
            label=_('skill'), queryset=Skill.objects.all(), 
            widget=widgets.LinkWidget())
    sex = filters.ChoiceFilter(
            label=_('sex'),
            choices=tuple([('', _('all'))]+list(Profile.SEX_TYPES)),
            widget=widgets.LinkWidget())
    user__last_login = filters.DateRangeFilter(
            label=_('last login'), widget=widgets.LinkWidget())
    tags = UniversalTagFilter(
            label=_('tags'), widget=widgets.LinkWidget())

    class Meta:
        model = Profile
        fields = [
                'skills',
                'sex',
                'user__last_login',
                'tags',
            ]

