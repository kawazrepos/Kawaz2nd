# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
from django import forms
from django.forms.models import construct_instance, InlineForeignKeyField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from ..db import models

__all__ = ['FormWithRequest', 'ModelFormWithRequest']

class FormWithRequest(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(FormWithRequest, self).__init__(*args, **kwargs)

class ModelFormWithRequest(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ModelFormWithRequest, self).__init__(*args, **kwargs)
    
    def _post_clean(self):
        opts = self._meta
        # Update the model instance with self.cleaned_data.
        self.instance = construct_instance(self, self.instance, opts.fields, opts.exclude)

        exclude = self._get_validation_exclusions()

        # Foreign Keys being used to represent inline relationships
        # are excluded from basic field value validation. This is for two
        # reasons: firstly, the value may not be supplied (#12507; the
        # case of providing new values to the admin); secondly the
        # object being referred to may not yet fully exist (#12749).
        # However, these fields *must* be included in uniqueness checks,
        # so this can't be part of _get_validation_exclusions().
        for f_name, field in self.fields.items():
            if isinstance(field, InlineForeignKeyField):
                exclude.append(f_name)

        # Clean the model instance's fields.
        try:
            if isinstance(self.instance, models.ModelWithRequest):
                self.instance.clean_fields(request=self.request, exclude=exclude)
            else:
                self.instance.clean_fields(exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)

        # Call the model instance's clean method.
        try:
            if isinstance(self.instance, models.ModelWithRequest):
                self.instance.clean(request=self.request)
            else:
                self.instance.clean()
        except ValidationError, e:
            self._update_errors({NON_FIELD_ERRORS: e.messages})

        # Validate uniqueness if needed.
        if self._validate_unique:
            self.validate_unique()
    def validate_unique(self, *args, **kwargs):
        exclude = self._get_validation_exclusions()
        try:
            if isinstance(self.instance, models.ModelWithRequest):
                self.instance.validate_unique(request=self.request, exclude=exclude)
            else:
                self.instance.validate_unique(exclude=exclude)
                
        except ValidationError, e:
            self._update_errors(e.message_dict)
            
    def save(self, commit=True):
        instance = super(ModelFormWithRequest, self).save(commit=False)
        if commit:
            if isinstance(instance, models.ModelWithRequest):
                instance.save(self.request)
            else:
                instance.save()
            self.save_m2m()
        return instance