# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Project, Category

class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'created_at')
    list_filter     = ('status',)
    search_fields   = ('title', 'body',)
admin.site.register(Project, ProjectAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display    = ('label', 'parent')
    search_fields   = ('label',)
admin.site.register(Category, CategoryAdmin)