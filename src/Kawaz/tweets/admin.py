# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Tweet

class TweetAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    fields          = ('body', 'reply',)
    list_display    = ('__unicode__', 'author', 'created_at',)
    list_filter     = ('author', 'source', 'created_at',)
    search_fields   = ('author__profile__nickname', 'author__username', 'body')
admin.site.register(Tweet, TweetAdmin)
