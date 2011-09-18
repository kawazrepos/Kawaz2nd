# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Message,MessageState

class MessageAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('title', 'author',)
    list_filter     = ('author', 'recivers',)
    search_fields   = ('title','body',)

class MessageStateAdmin(admin.ModelAdmin):
    list_display = ('user', 'message' ,'read',)
    
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageState, MessageStateAdmin)