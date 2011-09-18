# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Task

class TaskAdmin(admin.ModelAdmin):
    date_hierarchy  = 'deadline'
    list_display    = ('deadline', '__unicode__', 'status', 'publish_at', 'updated_at', 'created_at')
    list_filter     = ('pub_state', 'author', 'status', 'publish_at', 'created_at',)
    search_fields   = ('title', 'body', 'author',)
admin.site.register(Task, TaskAdmin)