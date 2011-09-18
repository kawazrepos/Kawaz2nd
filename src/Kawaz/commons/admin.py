# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Material

class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'license', 'pub_state', 'created_at', 'ip_address','pv',)
    list_filter     = ('pub_state', 'author', 'license',)
    search_fields   = ('title', 'body',)
admin.site.register(Material, MaterialAdmin)
