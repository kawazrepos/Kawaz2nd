from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from registration.admin import RegistrationAdmin as AdminBase
from models import RegistrationProfile


def create_random_password(length):
    import string
    from random import choice
    return ''.join([choice(string.letters + string.digits) for i in range(length)])

def get_site(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    return site

class RegistrationAdmin(AdminBase):
    actions = ['accept_users', 'reject_users', 'activate_users', 'resend_activation_email']
    list_display = ('user', 'activation_key_expired')
    raw_id_fields = ['user']
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not alrady
        activated.
        """
        site = get_site(request)
        for profile in queryset:
            password = create_random_password(10)
            RegistrationProfile.objects.accept_user(profile, site, send_email=False)
            RegistrationProfile.objects.activate_user(profile.activation_key)
            profile.user.set_password(password)
            profile.save()
            # Send activated email
            profile.send_activated_email(site, password=password)
    activate_users.short_description = _("Activate users")

    def accept_users(self, request, queryset):
        """
        Accept the selected users, if they are not already accepted.
        """
        site = get_site(request)
        for profile in queryset:
            RegistrationProfile.objects.accept_user(profile, site)
    accept_users.short_description = _('Accept users')

    def reject_users(self, request, queryset):
        """
        Reject the selected users, if they are not already rejected.
        """
        site = get_site(request)
        for profile in queryset:
            RegistrationProfile.objects.reject_user(profile, '', site)
    reject_users.short_description = _('Reject users')

admin.site.register(RegistrationProfile, RegistrationAdmin)
