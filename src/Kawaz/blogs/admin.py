# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy  = 'publish_at'
    fields          = ('pub_state', 'title', 'body')
    list_display    = ('__unicode__', 'pub_state', 'publish_at', 'updated_at')
    list_filter     = ('pub_state', 'author')
    search_fields   = ['title', 'body']

admin.site.register(Entry, EntryAdmin)