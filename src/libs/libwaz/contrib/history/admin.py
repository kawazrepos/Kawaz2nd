# -*- coding: utf-8 -*-
#
# Created:    2010/10/17
# Author:         alisue
#
from django.contrib import admin
from models import Timeline

class TimelineAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('label', 'url', 'action', 'user', 'created_at',)
    list_filter     = ('action', 'created_at', 'user')
admin.site.register(Timeline, TimelineAdmin)
