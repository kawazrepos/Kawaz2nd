# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django.contrib import admin

from models import Trackback

class TrackbackAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__', 'content_object', 'url', 'remote_ip', 'submit_date')
    list_filter     = ('content_type', 'object_id', 'remote_ip')
    search_fields   = ('object_id', 'remote_ip', 'url')
    date_hierarchy  = 'submit_date'
admin.site.register(Trackback, TrackbackAdmin)