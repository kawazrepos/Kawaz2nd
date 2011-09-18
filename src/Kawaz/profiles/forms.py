# -*- coding: utf-8 -*-
#
# Created:    2010/09/24
# Author:         alisue
#
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from models import Profile, Service

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = ('first_name', 'last_name', 'email')
        fields = ('email',)
        
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic 
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end 

        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.uf.fields['email'].required = True
        self.uf.fields['email'].help_text = u"運営側からの連絡時などで使用するため必ずアクセス可能なメールアドレスを指定してください（一般ユーザーには公開されません）"
        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
         
        # define fields order if needed
        self.fields.keyOrder = (
            'email',
            'pub_state', 'nickname', 'sex', 'skills', 'birthday', 'mood',
            'icon', 'place', 'location', 'url',
            'remarks',
        )

    def save(self, *args, **kwargs):
        # save both forms   
        self.uf.save(*args, **kwargs)
        return super(ProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = Profile

class ServiceForm(forms.ModelForm):
    class Media:
        js = (
            r'/javascript/plugins/jquery.formset.min.js',
            r'/javascript/plugins/jquery.formset.init.js'
        )
    class Meta:
        model = Service
        fields = (
            'service',
            'account',
            'pub_state',
        )
ServiceFormSet = inlineformset_factory(Profile, Service, extra=1, can_delete=True)  
        
def get_service_formset(form, formset=BaseInlineFormSet, *args, **kwargs):
    return inlineformset_factory(Profile, Service, form, formset, **kwargs)
