# -*- coding: utf-8 -*-
from libwaz import forms
from django.core import validators

from models import Tweet

class TweetAjaxForm(forms.ModelForm): 
    class Meta:
        model = Tweet
        fields = ('body', 'reply', 'source')
        widgets = {
            'reply':    forms.widgets.HiddenInput,
            'source':   forms.widgets.HiddenInput,
        }
class TweetForm(forms.ModelFormWithRequest): 
    class Meta:
        model = Tweet
        fields = ('body', 'reply', 'source')
        widgets = {
            'reply':    forms.widgets.HiddenInput,
            'source':   forms.widgets.HiddenInput,
        }
class FavoriteTweetForm(forms.Form):
    object_id   = forms.CharField(max_length=200, validators=[validators.validate_integer])
