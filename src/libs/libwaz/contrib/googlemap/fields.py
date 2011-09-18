# -*- coding: utf-8 -*-
#
# Created:    2010/09/06
# Author:         alisue
#
from django.forms import MultiValueField, fields

from widgets import GoogleMapWidget, HiddenGoogleMapWidget
from types import Location

class GoogleMapField(MultiValueField):
    widget          = GoogleMapWidget
    hidden_widget   = HiddenGoogleMapWidget
    
    def __init__(self, *args, **kwargs):
        field_list = (
            fields.DecimalField(max_value=90, min_value=-90, decimal_places=18, max_digits=25),
            fields.DecimalField(max_value=180, min_value=-180, decimal_places=18, max_digits=25),
            fields.IntegerField(),
        )
        if 'query_field_id' in kwargs:
            kwargs['widget'] = GoogleMapWidget(query_field_id=kwargs.pop('query_field_id'))

        super(GoogleMapField, self).__init__(field_list, *args, **kwargs)
        
    def compress(self, data_list):
        if not data_list:
            return ''
        return Location(data_list[0], data_list[1], data_list[2])
