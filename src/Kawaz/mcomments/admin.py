# -*- coding: utf-8 -*-
from django.contrib import admin
from models import MarkItUpComment

class MarkItUpCommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'submit_date'
    list_display    = ('__unicode__', 'comment', 'name')
    list_filter     = ('comment', 'user', 'user_name')
    search_fields   = ('comment', 'user', 'user_name')
admin.site.register(MarkItUpComment, MarkItUpCommentAdmin)