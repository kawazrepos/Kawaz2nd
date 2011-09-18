# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import fields
from types import Location

# TODO: Globalization

class GoogleMapField(models.Field):
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        if 'hidden' in kwargs:
            self.hidden = kwargs.pop('hidden')
        else:
            self.hidden = False
        if 'query_field_id' in kwargs:
            self.query_field_id = kwargs.pop('query_field_id')
        else:
            self.query_field_id = ''
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['help_text'] = kwargs.get('help_text', u"地図を投稿するには「地図を表示する」ボタンを押して地図を表示し"
                                         u"、マーカーをドラッグ＆ドロップで移動もしくは地図上で右クリックしてください。"
                                         u"また地図を破棄するには「地図を隠す」ボタンを押してください")
        super(GoogleMapField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if isinstance(value, Location):
            return value
        elif not value:
            return ''
        return Location.parse(value)
    
    def get_db_prep_value(self, value):
        return super(GoogleMapField, self).get_db_prep_value(str(value))
        
    def get_internal_type(self):
        return 'CharField'
    
    def formfield(self, **kwargs):
        # メソッドの呼び出し側がデフォルトをオーバライド
        # できるようにするための標準的な書き方
        defaults = {'form_class': fields.GoogleMapField, 'query_field_id': self.query_field_id}
        defaults.update(kwargs)
        return super(GoogleMapField, self).formfield(**defaults)
    
    def contribute_to_class(self, cls, name):
        super(GoogleMapField, self).contribute_to_class(cls, name)
        setattr(cls, 'get_%s_display' % self.name, lambda cls, self=self, name=name: self._get_googlemap_display(cls, name))
        setattr(cls, 'get_%s_link' % self.name, lambda cls, self=self, name=name: self._get_googlemap_link(cls, name))
    
    def _get_googlemap_display(self, cls, name):
        try:
            body = render_to_string(r'googlemap/googlemap.html', {
                'class_name':   settings.GOOGLEMAP_CLASS_NAME,
                'latitude':     getattr(cls, name).latitude,
                'longitude':    getattr(cls, name).longitude,
                'zoom':         getattr(cls, name).zoom,
                'hidden':       '' if not self.hidden else 'hidden',
                'editable':     ''
            })
            return mark_safe(body)
        except:
            # Fail silently
            return ''
    def _get_googlemap_link(self, cls, name):
        url = u"""<a href="http://maps.google.co.jp/maps?near=%(latitude)s,%(longitude)s&z=%(zoom)s" target="_blank">Google Mapsで表示する</a>"""
        try:
            kwargs = {
                'latitude':     getattr(cls, name).latitude,
                'longitude':    getattr(cls, name).longitude,
                'zoom':         getattr(cls, name).zoom,
            }
            return mark_safe(url % kwargs)
        except:
            
            return ''
        