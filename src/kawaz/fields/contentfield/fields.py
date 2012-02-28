#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
A Richarea TextField used in Kawaz


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf import settings

from markupfield.fields import MarkupField
from markitup.widgets import MarkItUpTextarea

settings.CONTENTFIELD_DEFAULT_MARKUP_TYPE = \
        getattr(settings, 'CONTENTFIELD_DEFAULT_MARKUP_TYPE', 'markdown')

class ContentField(MarkupField):
    """A Richtext field used in Kawaz"""
    def __init__(self, *args, **kwargs):
        if not 'markup_type' in kwargs:
            # Set markup type that the field will always use, 
            # editable=False is set on the hidden field so it is not shown in ModelForms.
            kwargs['markup_type'] = settings.CONTENTFIELD_DEFAULT_MARKUP_TYPE
        super(ContentField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
                'widget': MarkItUpTextarea
            }
        defaults.update(kwargs)
        return super(ContentField, self).formfield(**defaults)

    def go_db_prep_value(self, connection, *args, **kwargs):
        return super(ContentField, self).go_db_prep_value(*args, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^kawaz.core.fields.contentfield.ContentField"])
except ImportError:
    pass

