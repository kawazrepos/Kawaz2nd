# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/13
#
from django import forms
from django.contrib.auth.models import Group
from django.contrib import messages

from ..markitupfield.widgets import MarkItUpTextarea

class EmailForm(forms.Form):
    sender      = forms.EmailField(label=u"送信者のメールアドレス", 
                                   help_text=u"返信時にこのメールアドレス宛にメールを送信するので普段ご利用のメールアドレスを入力してください")
    subject     = forms.CharField(label=u"題名", max_length=250,
                                  help_text=u"件名のみで要件がわかるように書いてください")
    body        = forms.CharField(label=u"本文", widget=MarkItUpTextarea,
                                 help_text=u"メールの本文です。HTML形式ではなくMarkdown形式で送信されるのでご注意ください")