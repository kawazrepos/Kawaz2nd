# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/15
#
from django import forms

def errors_append(form, field_name, message):
    u'''
    Add an ValidationError to a field (instead of __all__) during Form.clean():

    class MyForm(forms.Form):
        def clean(form):
            value_a=form.cleaned_data['value_a']
            value_b=form.cleaned_data['value_b']
            if value_a==... and value_b==...:
                formutils.errors_append(form, 'value_a', u'Value A must be ... if value B is ...')
            return form.cleaned_data
    '''
    assert form.fields.has_key(field_name), field_name
    error_list=form.errors.get(field_name)
    if error_list is None:
        error_list=forms.util.ErrorList()
        form.errors[field_name]=error_list
    error_list.append(message)