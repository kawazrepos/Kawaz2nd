# -*- coding: utf-8 -*-
#
# Created:    2010/09/24
# Author:         alisue
#
from django.contrib import admin

from models import Profile,Service, Skill

class ServiceInline(admin.TabularInline):
    model = Service
    verbose_name = u"サービス"
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('nickname', 'user', 'sex', 'birthday', 'created_at','is_authenticated_twitter')
    list_filter     = ('sex', 'skills',)
    search_fields   = ('nickname', 'user__username', 'mood', 'remarks')
    inlines         = (ServiceInline,)
admin.site.register(Profile, ProfileAdmin)



class ServiceAdmin(admin.ModelAdmin):
    list_display    = ('service', 'account', 'profile',)
    list_filter     = ('service', 'profile',)
    search_fields   = ('account', 'profile',)
admin.site.register(Service, ServiceAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
    search_fields   = ('label',)
admin.site.register(Skill, SkillAdmin)