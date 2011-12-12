# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/forms.py
# created by giginet on 2011/11/06
#
from django.forms.fields import ImageField

class ThumbnailFormField(ImageField):
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(ThumbnailFormField, self).clean(data, initial)
        else:
            return '__deleted__'
