# -*- coding: utf-8 -*-
#
# Created:    2010/10/12
# Author:         alisue
#
from django.db import models

def reverse_model(fn, request, *args, **kwargs):
    if fn.__name__ == 'object_detail':
        if 'queryset' in kwargs:
            queryset = kwargs['queryset']
        elif 'model' in kwargs:
            queryset = kwargs['model'].objects
        elif 'form_class' in kwargs:
            queryset = kwargs['form_class']._meta.model.objects
        else:
            return None
        if 'year' in kwargs and 'month' in kwargs and 'day' in kwargs and 'date_field' in kwargs:
            # date_based
            queryset = queryset.filter(**{
                "%s__year"%kwargs['date_field']: kwargs['year'],
                "%s__month"%kwargs['date_field']: kwargs['month'],
                "%s__day"%kwargs['date_field']: kwargs['day']
            })
        if 'object_id' in kwargs:
            try:
                obj = queryset.get(pk=kwargs['object_id'])
                return obj
            except Exception, e:
                pass
        elif 'slug' in kwargs:
            slug = kwargs['slug']
            slug_field = kwargs.get('slug_field', 'slug')
            try:
                obj = queryset.get(**{slug_field: slug,})
                return obj
            except Exception, e:
                pass
    else:
        return None