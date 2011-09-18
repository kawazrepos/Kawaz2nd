# -*- coding: utf-8 -*-
#
# NOTICE:
#  `django import forms`の代わりに指定
#
from libwaz import forms
from models import Announcement

class AnnouncementForm(forms.ModelFormWithRequest):
    class Meta:
        model   = Announcement
        fields  = ('pub_state', 'title', 'body', 'sage')