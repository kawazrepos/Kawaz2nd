# -*- coding: utf-8 -*-
from libwaz import forms

from models import Event

class EventForm(forms.ModelFormWithRequest):
    class Meta:
        model = Event
        fields = (
            'pub_state',
            'title', 'body', 
            'period_start', 'period_end',
            'place', 'location',
        )
