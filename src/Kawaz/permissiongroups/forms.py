# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django import forms
from django.contrib.auth.models import User, Permission

import models

class PermissionGroupForm(forms.ModelForm):
    users       = forms.ModelMultipleChoiceField(label="所属ユーザー",
                                                 queryset=User.objects.filter(is_active=True),
                                                 required=False,
                                                 help_text=u"このパーミッショングループに所属しているユーザーです。Ctrlキーで複数選択可能です")
    permissions = forms.ModelMultipleChoiceField(label="所有パーミッション",
                                                 queryset=Permission.objects.all(),
                                                 required=False,
                                                 help_text=u"このパーミッショングループが所有しているパーミッションです。Ctrlキーで複数選択可能です")
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
        instance.users.clear()
        for user in self.cleaned_data['users']:
            instance.users.add(user)
        instance.permissions.clear()
        for permission in self.cleaned_data['permissions']:
            instance.permissions.add(permission)
        instance.save()
        return instance
    
class PartialPermissionGroupForm(PermissionGroupForm):
    class Meta:
        model = models.PermissionGroup
        fields = ('users', 'permissions')