# -*- coding: utf-8 -*-
#    
#    
#    created by giginet on 2011/07/20
#
from django.contrib import admin
from models import Star

class StarAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    fields          = ('comment', 'color')
    list_display    = ('content_object', 'author', 'color',)
    list_filter     = ('content_object', 'author')
    search_fields   = ['comment', 'author']

admin.site.register(Star, StarAdmin)