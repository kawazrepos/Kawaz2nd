# -*- coding: utf-8 -*-
#    
#    django_star_demo.blogs.admin
#    created by giginet on 2011/09/20
#
from django.contrib import admin

from models import Star

class StarAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'author', 'comment')
    search_fields = ('content_object',)
    filter_fields = ('author',)
admin.site.register(Star, StarAdmin)