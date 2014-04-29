# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
import re
from django import forms
from django.core.exceptions import ValidationError

from ..markitupfield.widgets import MarkItUpTextarea

JAPANESE_PATTERN = u'[一-龠ァ-ヶーぁ-んｱ-ﾝﾞﾟ]+'

class EmailForm(forms.Form):
    sender      = forms.EmailField(label=u"送信者のメールアドレス",
                                   help_text=u"返信時にこのメールアドレス宛にメールを送信するので普段ご利用のメールアドレスを入力してください")
    subject     = forms.CharField(label=u"題名", max_length=250,
                                  help_text=u"件名のみで要件がわかるように書いてください")
    body        = forms.CharField(label=u"本文", widget=MarkItUpTextarea,
                                 help_text=u"メールの本文です。HTML形式ではなくMarkdown形式で送信されるのでご注意ください")

    def is_valid(self):
        b = super(EmailForm, self).is_valid()
        body = self.cleaned_data['body']
        if not re.search(JAPANESE_PATTERN, body, re.U): # SPAM防止のため、一切日本語が含まれていない書き込みはrejectする
            raise ValidationError(u'日本語が含まれていないお問い合わせは送信することができません')
        return b
