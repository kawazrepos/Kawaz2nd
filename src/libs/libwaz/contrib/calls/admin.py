# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Call

class CallAdmin(admin.ModelAdmin):
    list_display    = ('url', 'label', 'content_object', 'user_to', 'user_from', 'read', 'created_at')
    list_filter     = ('url', 'label', 'user_to', 'user_from', 'created_at')
admin.site.register(Call, CallAdmin)
