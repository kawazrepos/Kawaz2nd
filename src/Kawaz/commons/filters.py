# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/03
#
from libwaz import forms
from libwaz.contrib.siever import filters

class FiletypeFilter(filters.ChoiceFilter):
    """
    This filter preforms an OR query on the selected options.
    """
    field_class = forms.ChoiceField
    def __init__(self, threshold=1, *args, **kwargs):
        self.threshold = threshold
        super(FiletypeFilter, self).__init__(*args, **kwargs)
    @property
    def field(self):
        choices = (
            ('', u"全て"),
            ('image',   u"画像"),
            ('audio',   u"サウンド"),
            ('movie',   u"ムービー"),
            ('archive', u"圧縮ファイル"),
            ('text',    u"テキスト"),
            ('application', u"アプリケーション")
        )
        self.extra['choices'] = choices
        return super(FiletypeFilter, self).field
    
    def filter(self, qs, value):
        if not value:
            return qs
        elif not isinstance(value, list) and not isinstance(value, tuple):
            value = [value]
        ids = []
        for item in qs.all():
            if item.filetype() in value:
                ids.append(item.pk)
        return qs.filter(pk__in=ids)