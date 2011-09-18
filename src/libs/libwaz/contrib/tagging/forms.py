# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
# -*- coding: utf-8 -*-
from django import forms

class MultiTagForm(forms.Form):
    content_type    = forms.IntegerField(widget=forms.HiddenInput)
    object_id       = forms.CharField(widget=forms.HiddenInput)
    labels          = forms.CharField(widget=forms.HiddenInput)