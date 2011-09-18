# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/08
#
from django import forms
from django.contrib.auth.models import User

class EmailUsersForm(forms.Form):
    recivers = forms.ModelMultipleChoiceField(label=u"送信先", queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    subject = forms.CharField(label="題名")
    body = forms.CharField(label="本文", widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(EmailUsersForm, self).__init__(*args, **kwargs)
        def get_name(user):
            profile  = user.get_profile()
            if profile.nickname is None:
                return u"%sさん (未登録ユーザー)" % user.username
            elif not user.is_active:
                return u"%sさん (退会済みユーザー)" % profile.nickname
            else:
                return u"%sさん" % profile.nickname
        self.fields['recivers'].choices = [
            (user.pk, get_name(user)) for user in User.objects.exclude(email='')
        ]