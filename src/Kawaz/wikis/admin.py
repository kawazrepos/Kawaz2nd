# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy  = 'updated_at'
    list_display    = ('title', 'author', 'updated_by', 'created_at', 'updated_at')
    list_filter     = ('project', 'pub_state', 'permission', 'author',)
    search_fields   = ['title', 'body']
admin.site.register(Entry, EntryAdmin)