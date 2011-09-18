# -*- coding: utf-8 -*-
#
# Created:        2010/11/08
# Author:        alisue
#
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration.backends import get_backend as _get_backend
from registration.backends.default import DefaultBackend

from models import RegistrationProfile
from forms import RegistrationForm, RegistrationFormTermsOfService
import signals

def get_backend(backend):
    if isinstance(backend, basestring):
        return _get_backend(backend)
    return backend()

class ThreeStepBackend(DefaultBackend):
    
    @staticmethod
    def _get_current_site(request):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        return site
    
    def register(self, request, **kwargs):
        username, email, password, remarks = kwargs['username'], kwargs['email'], kwargs['password1'], kwargs['remarks']
        site = ThreeStepBackend._get_current_site(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=username,
            email=email,
            password=password, 
            remarks=remarks,
            site=site,
            send_email=True)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
    
    def approve(self, request, registration_profiles):
        site = ThreeStepBackend._get_current_site(request)
        success_users = []
        for registration_profile in registration_profiles:
            user = RegistrationProfile.objects.approve_user(
                registration_profile=registration_profile,
                site=site,
                send_email=True)
            if user:
                signals.user_approved.send(sender=self.__class__,
                                           user=user,
                                           request=request)
                success_users.append(user)
        return success_users
    
    def reject(self, request, registration_profiles):
        site = ThreeStepBackend._get_current_site(request)
        success_users = []
        for registration_profile in registration_profiles:
            user = RegistrationProfile.objects.reject_user(
                registration_profile=registration_profile,
                site=site,
                send_email=True)
            if user:
                signals.user_rejected.send(sender=self.__class__,
                                           user=user,
                                           request=request)
                success_users.append(user)
        return success_users
    
    def activate(self, request, activation_key):
        site = ThreeStepBackend._get_current_site(request)
        activated = RegistrationProfile.objects.activate_user(activation_key, site)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.
        
        """
        #return RegistrationForm
        return RegistrationFormTermsOfService
    
    def post_approvation_redirect(self, request, success_users, failed_users):
        return ('registration_handle', (), {'success_users': success_users, 'failed_users': failed_users})
    def post_rejection_redirect(self, request, success_users, failed_users):
        return ('registration_handle', (), {'success_users': success_users, 'failed_users': failed_users})