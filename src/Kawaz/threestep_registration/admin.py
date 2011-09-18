# -*- coding: utf-8 -*-
#
# Created:        2010/11/08
# Author:        alisue
#
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered, AlreadyRegistered
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from registration.models import RegistrationProfile as _RegistrationProfile
from models import RegistrationProfile


class RegistrationAdmin(admin.ModelAdmin):
    actions = ['activate_users', 'resend_activation_email', 'approve_users', 'reject_users']
    list_display = ('user', 'activation_key_expired', 'status')
    list_filter = ('status',)
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name')

    @classmethod
    def _get_current_site(cls, request):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        return site
    
    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        site = RegistrationAdmin._get_current_site(request)
        for profile in queryset:
            RegistrationProfile.objects.activate_user(profile.activation_key, site)
    activate_users.short_description = _("Activate users")
    
    def approve_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        site = RegistrationAdmin._get_current_site(request)
        for profile in queryset:
            RegistrationProfile.objects.approve_user(profile.user.username, site)
    approve_users.short_description = _("Approve users")
    
    def reject_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        
        """
        site = RegistrationAdmin._get_current_site(request)
        for profile in queryset:
            RegistrationProfile.objects.reject_user(profile.user.username, site)
    reject_users.short_description = _("Reject users")
    
    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.
        
        """
        site = RegistrationAdmin._get_current_site(request)
        for profile in queryset:
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = _("Re-send activation emails")

try:
    admin.site.unregister(_RegistrationProfile)
except NotRegistered:
    pass
try:
    admin.site.register(RegistrationProfile, RegistrationAdmin)
except AlreadyRegistered:
    pass
