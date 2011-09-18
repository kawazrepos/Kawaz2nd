# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/27
#
from django.contrib.contenttypes.generic import GenericRelation

from models import TaggedItem

class TaggingField(GenericRelation):
    u"""TaggedItem field for model (Reverse generic relation)"""
    def __init__(self, **kwargs):
        if not 'to' in kwargs:
            kwargs['to'] = TaggedItem
        super(TaggingField, self).__init__(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r'libwaz.contrib.tagging.fields.TaggingField'])
except ImportError:
    pass
