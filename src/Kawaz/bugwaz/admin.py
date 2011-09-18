# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/10/30
#
from django.contrib import admin
from models import Component, Version, Product, Report

admin.site.register(Component)
admin.site.register(Version)
admin.site.register(Product)

class ReportAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'product', 'component', 'version', 'serverity', 'os', 'status', 'resolution', 'priority', 'ip_address')
    list_filter     = ('author', 'product', 'component', 'version', 'serverity', 'os', 'status', 'resolution', 'priority')
    search_fields   = ('label', 'body', 'ip_address')
admin.site.register(Report, ReportAdmin)