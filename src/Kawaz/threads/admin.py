# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Thread

class ThreadAdmin(admin.ModelAdmin):
    date_hierarchy      = 'updated_at'
    list_display        = ('__unicode__', 'project', 'pub_state', 'publish_at', 'updated_at')
    list_filter         = ('pub_state', 'author',)
    search_fields       = ['title', 'body',]
admin.site.register(Thread, ThreadAdmin)