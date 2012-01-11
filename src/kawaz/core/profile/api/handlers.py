#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
API Handler via piston for profile application


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
from django import forms
from piston.handler import BaseHandler
from piston.utils import throttle
from piston.utils import validate

from ..models import Profile

class ProfileMoodValidationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mood',)

class ProfileMoodHandler(BaseHandler):
    """Authenticated entrypoint for profile"""
    allowed_methods = ('PUT',)
    fields = ('pk', 'mood',)
    model = Profile

    @validate(ProfileMoodValidationForm)
    @throttle(5, 100) # allow 5 times in 100 sec
    def update(self, request):
        profile = request.user.profile

        profile.mood = request.PUT.get('mood', profile.mood)
        profile.save()
        return profile
