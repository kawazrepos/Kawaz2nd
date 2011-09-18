# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/06
#
from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
#from django.contrib.auth.models import User

__all__ = ['ModelWithRequest',]

import signals

class ModelWithRequest(models.Model):
    class Meta:
        abstract = True
    
    def full_clean(self, exclude=None, request=None):
        """
        Calls clean_fields, clean, and validate_unique, on the model,
        and raises a ``ValidationError`` for any errors that occured.
        """
        errors = {}
        if exclude is None:
            exclude = []

        try:
            self.clean_fields(request=request, exclude=exclude)
        except ValidationError, e:
            errors = e.update_error_dict(errors)

        # Form.clean() is run even if other validation fails, so do the
        # same with Model.clean() for consistency.
        try:
            self.clean(request=request)
        except ValidationError, e:
            errors = e.update_error_dict(errors)

        # Run unique checks, but only for fields that passed validation.
        for name in errors.keys():
            if name != NON_FIELD_ERRORS and name not in exclude:
                exclude.append(name)
        try:
            self.validate_unique(request=request, exclude=exclude)
        except ValidationError, e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)
        
    def clean_fields(self, request=None, *args, **kwargs):
        super(ModelWithRequest, self).clean_fields(*args, **kwargs)
    def clean(self, request=None, *args, **kwargs):
        super(ModelWithRequest, self).clean(*args, **kwargs)
    def validate_unique(self, request=None, *args, **kwargs):
        super(ModelWithRequest, self).validate_unique(*args, **kwargs)
        
    def save(self, request=None, *args, **kwargs):
        if self.pk is None:
            created = True
        else:
            created = False
        signals.pre_save.send(sender=self, instance=self, request=request)
        super(ModelWithRequest, self).save(*args, **kwargs)
        signals.post_save.send(sender=self, instance=self, created=created, request=request)
    
    def delete(self, request=None, *args, **kwargs):
        signals.pre_delete.send(sender=self, instance=self, request=request)
        super(ModelWithRequest, self).delete(*args, **kwargs)
        signals.post_delete.send(sender=self, instance=self, request=request)