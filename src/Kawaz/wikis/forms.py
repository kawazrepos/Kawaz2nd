# -*- coding: utf-8 -*-
from libwaz import forms
from models import Entry

class EntryForm(forms.ModelFormWithRequest):
    class Meta:
        model = Entry
        fields = ('pub_state', 'permission', 'title', 'body', 'project',)
    def __init__(self, request, *args, **kwargs):
        super(EntryForm, self).__init__(request, *args, **kwargs)
        if kwargs.get('initial') and 'project' in kwargs['initial']:
            self.fields['project'].widget = forms.HiddenInput()
        else:
            self.fields['project'].queryset = request.user.projects_joined.all()