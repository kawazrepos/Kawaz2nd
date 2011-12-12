#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Form class of Profile


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
from django.conf import settings
from django import forms
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.auth.models import User
from django.utils.text import ugettext_lazy as _

import models

class ProfileForm(forms.ModelForm):
    """profile form class"""
    class Meta:
        model = models.Profile
    class InnerUserForm(forms.ModelForm):
        """this class is used for binding class of ProfileForm"""
        class Meta:
            model = User
            fields = ('email',)
    def __init__(self, *args, **kwargs):
        # create inner UserForm instance
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = self.InnerUserForm(*args, **user_kwargs)

        super(ProfileForm, self).__init__(*args, **kwargs)

        self.uf.fields['email'].required = True
        self.uf.fields['email'].help_text = \
                _('Please input your available e-mail address.'
                  'It is only used in managment reason (Non published)')
        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

        # define fields order if needed
        self.fields.keyOrder = (
                'pub_state', 'nickname', 'email',
                'sex', 'skills', 'birthday', 'mood',
                'icon', 'place', 'location', 'url',
                'remarks',)
    def save(self, *args, **kwargs):
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)

class ServiceForm(forms.ModelForm):
    class Media:
        js = (
                r"%sjavascript/plugins/jquery.formset.min.js" %
                settings.MEDIA_ROOT,
                r"%sjavascript/plugins/jquery.formset.init.js" %
                settings.MEDIA_ROOT,
            )
    class Meta:
        model = models.Service
        fields = ('service', 'account', 'pub_state')
ServiceFormSet = inlineformset_factory(models.Profile, models.Service,
                                       extra=1, can_delete=True)

def get_service_formset(form, formset=BaseInlineFormSet, *args, **kwargs):
    return inlineformset_factory(
            models.Profile, models.Service,
            form, formset, **kwargs)
                
