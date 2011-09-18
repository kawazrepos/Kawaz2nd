# -*- coding: utf-8 -*-
from libwaz import forms
from models import Material

class MaterialForm(forms.ModelFormWithRequest):
    class Meta:
        model = Material
        fields = (
                  'project', 'pub_state', 'license', 'title', 'file', 'body',
        )
    def __init__(self, request, *args, **kwargs):
        super(MaterialForm, self).__init__(request, *args, **kwargs)
        if kwargs.get('initial') and 'project' in kwargs['initial']:
            self.fields['project'].widget = forms.HiddenInput()
        else:
            self.fields['project'].queryset = request.user.projects_joined.all()
            
class AttachementMaterialForm(forms.ModelFormWithRequest):
    class Meta:
        model   = Material
        fields  = ('file',)
