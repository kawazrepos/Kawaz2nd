#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


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

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite

from registration.backends.default import DefaultBackend as BackendBase

from registration.signals import user_registered
from registration2.models import RegistrationProfile
from registration2.signals import user_accepted
from registration2.signals import user_rejected

from registration2.forms import RegistrationForm

def get_site(request):
    if Site._meta.installed:
        return Site.objects.get_current()
    else:
        return RequestSite(request)

class DefaultBackend(BackendBase):
    def register(self, request, username, email):
        site = get_site(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
                username, email, site
            )

        user_registered.send(sender=self.__class__,
                             user=new_user,
                             request=request)

        return new_user

    def accept(self, request, registration_profile):
        site = get_site(request)
        RegistrationProfile.objects.accept_user(
                registration_profile=registration_profile,
                site=site,
                send_email=True
            )
        user_accepted.send(sender=self.__class__,
                           user=registration_profile.user,
                           request=request)

    def reject(self, request, registration_profile, reason):
        site = get_site(request)
        RegistrationProfile.objects.reject_user(
                registration_profile=registration_profile,
                reason=reason,
                site=site,
                send_email=True
            )
        user_rejected.send(sender=self.__class__,
                           user=registration_profile.user,
                           reason=reason,
                           request=request)

    def is_valid_activation_key(self, activation_key):
        profile = RegistrationProfile.objects.get_by_activation_key(activation_key)
        return profile != None

    def activate(self, request, activation_key, password):
        activated = super(DefaultBackend, self).activate(request, activation_key)
        if activated:
            activated.set_password(password)
        return activated

    def get_form_class(self, request):
        return RegistrationForm
