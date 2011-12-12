#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
admin module for django-admin


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.contrib import admin
from django.utils.text import ugettext_lazy as _

import models


class SkillAdmin(admin.ModelAdmin):
    """Admin class for skill in django-admin"""
    list_display = ('__unicode__',)
    search_fields = ('label',)
admin.site.register(models.Skill, SkillAdmin)


class ProfileAdmin(admin.ModelAdmin):
    """Admin class for profile in django-admin"""
    class ServiceInline(admin.TabularInline):
        """Inline class for service in django-admin"""
        model = models.Service
        verbose_name = _('service')
        verbose_name_plural = _('services')
        extra = 0
    date_hierarchy = 'created_at'
    list_display = (
            'nickname', 'user', 'sex', 'birthday', 'created_at',
            'is_authenticated_twitter')
    list_filter = ('sex', 'skills', 'user__last_login')
    search_fields = ('nickname', 'user__username', 'mood', 'remarks')
    inlines = (ServiceInline,)
admin.site.register(models.Profile, ProfileAdmin)


class ServiceAdmin(admin.ModelAdmin):
    """Admin class for service in django-admin"""
    list_display = ('service', 'account', 'profile',)
    list_filter = ('service', 'profile',)
    search_fields = ('account', 'profile')
admin.site.register(models.Service, ServiceAdmin)
