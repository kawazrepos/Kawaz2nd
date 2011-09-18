# -*- coding: utf-8 -*-
#
# from snippets: http://djangosnippets.org/snippets/1054/
#
from django.contrib import admin

from models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('title', 'author', 'created_at', 'updated_at', 'sage')
    list_filter     = ('author', 'created_at', 'updated_at')
    search_fields   = ('title', 'body', 'author',)
    
    def queryset(self, request):
        qs = super(AnnouncementAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author = request.user)
    
    def save_model(self, request, obj, form, change):
        obj.save(request)
    
    def has_change_permission(self, request, obj=None):
        if not obj:
            return True     # So they can see the change list page
        if request.user.is_superuser or obj.author == request.user:
            return True
        return False
    has_delete_permission = has_change_permission
    
admin.site.register(Announcement, AnnouncementAdmin)
