# -*- coding: utf-8 -*-
from libwaz import forms

from models import Thread

class ThreadForm(forms.ModelFormWithRequest):
    class Meta:
        model = Thread
        fields = (
            'project', 'pub_state', 'permission', 'title', 'body',
        )
    def __init__(self, request, *args, **kwargs):
        super(ThreadForm, self).__init__(request, *args, **kwargs)
        if kwargs.get('initial') and 'project' in kwargs['initial']:
            self.fields['project'].widget = forms.HiddenInput()
        else:
            self.fields['project'].queryset = request.user.projects_joined.all()
