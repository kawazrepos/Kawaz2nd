# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Tag, TaggedItem

class TagAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
    search_fields   = ('label',)
admin.site.register(Tag, TagAdmin)

class TaggedItemAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__', 'content_object', 'content_type', 'frozen', 'order')
    list_filter     = ('content_type', 'frozen',)
admin.site.register(TaggedItem, TaggedItemAdmin)
