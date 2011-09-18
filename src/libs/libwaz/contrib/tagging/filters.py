# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/03
#
from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from models import Tag
from utils import parse_tag_input

try:
    from libwaz.contrib.siever import filters
except ImportError:
    from django_filters import filters

class TaggingFilter(filters.ChoiceFilter):
    """
    This filter preforms an OR query on the selected options.
    """
    field_class = forms.ChoiceField
    def __init__(self, threshold=1, *args, **kwargs):
        self.threshold = threshold
        super(TaggingFilter, self).__init__(*args, **kwargs)
    @property
    def field(self):
        qs = Tag.objects.get_for_model(self.model).annotate(count=Count('items')).exclude(count__lt=self.threshold).order_by('-count')
        choices = [['', _('All')]] + [(tag.pk, tag.label) for tag in qs]
        self.extra['choices'] = choices
        return super(TaggingFilter, self).field
    
    def filter(self, qs, value):
        if not value:
            return qs
        if isinstance(value, basestring):
            value = parse_tag_input(value)
        elif not isinstance(value, list) and not isinstance(value, tuple):
            value = [value]
        return qs.filter(**{"%s__tag__pk__in"%self.name: value}).distinct()