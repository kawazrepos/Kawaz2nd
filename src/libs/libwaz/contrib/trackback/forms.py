# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django import forms
from models import Trackback

class TrackbackForm(forms.ModelForm):
    class Meta:
        model = Trackback