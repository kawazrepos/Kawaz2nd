# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Event

class EventAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    fields          = ('pub_state', 'title', 'body', 'period_start', 'period_end', 'place', 'location')
    list_display    = ('title', 'author', 'place', 'get_period_display', 'is_active', 'created_at', 'publish_at')
    list_filter     = ('period_start', 'period_end', 'pub_state')
    search_fields   = ('title', 'body', 'author__username', 'place', 'created_at', 'publish_at')
admin.site.register(Event, EventAdmin)