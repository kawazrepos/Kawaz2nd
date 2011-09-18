# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/29
#
from django.conf import settings
from decimal import Decimal

# TODO: Globalization

class Location(object):
    @classmethod
    def parse(cls, value):
        u"""'latitude,longitude,zoom'というフォーマットの文字列からLocationオブジェクトをパースする"""
        if isinstance(value, basestring):
            # TODO: Validation
            latitude, longitude, zoom = value.split(',')
            return cls(Decimal(latitude), Decimal(longitude), int(zoom))
        else:
            return value
    @classmethod
    def default(cls):
        return cls()
    
    def __init__(self, latitude=None, longitude=None, zoom=None):
        self.latitude = latitude or settings.GOOGLEMAP_DEFAULT_LATITUDE
        self.longitude = longitude or settings.GOOGLEMAP_DEFAULT_LONGITUDE
        self.zoom = zoom or settings.GOOGLEMAP_DEFAULT_ZOOM
        
    def __str__(self):
        return self.__unicode__().encode('utf-8')
    
    def __unicode__(self):
        return u"%s, %s ,%d" % (
            self.latitude, 
            self.longitude,
            self.zoom,
        )