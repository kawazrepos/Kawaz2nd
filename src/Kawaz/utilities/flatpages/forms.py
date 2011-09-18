# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/09
#
from django import forms
from django.contrib.flatpages.models import FlatPage

from ...markitupfield.widgets import MarkItUpTextarea

class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        exclude = ('template_name',)
    
    def __init__(self, *args, **kwargs):
        super(FlatPageForm, self).__init__(*args, **kwargs)
        self.fields['content'].help_text = u"書きやすいようにTanixエディタを使っていますが、フラットページをMarkdownで記述することはできません"
        self.fields['content'].widget = MarkItUpTextarea()
        self.fields['sites'].initial = [1, 2]
        self.fields['sites'].help_text = u"公開するサイトを指定します。通常は'www.kawaz.tk'が選択されていれば問題ありません"