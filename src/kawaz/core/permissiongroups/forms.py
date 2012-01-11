#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Form class of PermissionGroup


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
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.utils.text import ugettext_lazy as _

import models

class PermissionGroupForm(forms.ModelForm):
    """permission group form class"""
    users = forms.ModelMultipleChoiceField(
            label=_('Users belong to'),
            queryset=User.objects.filter(is_active=True),
            required=False)
    permissions = forms.ModelMultipleChoiceField(
            label=_('Permissions belong to'),
            queryset=Permission.objects.all(),
            required=False)

    class Meta:
        model = models.PermissionGroup
        
    def __init__(self, *args, **kwargs):
        super(PermissionGroupForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance', None):
            instance = kwargs['instance']
            self.fields['users'].initial = [user.pk for user in instance.users.all()]
            self.fields['permissions'].initial = [permission.pk for permission in instance.permissions.all()]
    
    def save(self, *args, **kwargs):
        instance = super(PermissionGroupForm, self).save(*args, **kwargs)
        # Add users and permissions
        instance.users.clear()
        for user in self.cleaned_data['users']:
            instance.users.add(user)
        instance.permissions.clear()
        for permission in self.cleaned_data['permissions']:
            instance.permissions.add(permission)
        instance.save()
        return instance
    
class PartialPermissionGroupForm(PermissionGroupForm):
    """partial form of permission group"""
    class Meta:
        model = models.PermissionGroup
        fields = ('users', 'permissions')
