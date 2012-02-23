# vim: set fileencoding=utf8:
"""
Models of registration-request


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
__VERSION__ = "0.1.0"
import random
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.text import ugettext_lazy as _

from registration.models import SHA1_RE
from registration.models import RegistrationProfile as ProfileBase
from registration.models import RegistrationManager as ManagerBase

class RegistrationManager(ManagerBase):
    def get_by_activation_key(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return None
            if not profile.activation_key_expired():
                return profile
        return None

    def untreated(self):
        return self.filter(activation_key=self.model.UNTREATED)

    def activated(self):
        return self.filter(activation_key=self.model.ACTIVATED)

    def accepted(self):
        activation_keys = (
                self.model.UNTREATED,
                self.model.REJECTED,
                self.model.ACTIVATED,
            )
        return self.exclude(activation_key__in=activation_keys)

    def rejected(self):
        return self.filter(activation_key=self.model.REJECTED)

    def activate_user(self, activation_key):
        profile = self.get_by_activation_key(activation_key)
        if profile:
            user = profile.user
            user.is_active = True
            user.save()
            profile.activation_key = self.model.ACTIVATED
            profile.save()
            return user
        return False

    def accept_user(self, registration_profile, site, send_email=True):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = registration_profile.user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = sha_constructor(salt+username).hexdigest()
        registration_profile.activation_key = activation_key
        registration_profile.save()

        if send_email:
            registration_profile.send_acception_email(site)

    def reject_user(self, registration_profile, reason, site, send_email=True):
        registration_profile.activation_key = self.model.REJECTED
        registration_profile.save()

        if send_email:
            registration_profile.send_rejection_email(reason, site)

    @transaction.commit_on_success
    def create_inactive_user(self, username, email, site, send_email=True):
        new_user = super(RegistrationManager, self).create_inactive_user(
                username=username,
                email=email,
                password='password',
                site=site,
                send_email=send_email
            )
        new_user.set_unusable_password()
        new_user.save()

        return new_user

    def create_profile(self, user):
        registration_profile = super(RegistrationManager, self).create_profile(user)
        registration_profile.activation_key = self.model.UNTREATED
        registration_profile.save()
        return registration_profile


class RegistrationProfile(ProfileBase):
    UNTREATED = u"UNTREATED_YET"
    REJECTED = u"ALREADY_REJECTED"

    objects = RegistrationManager()

    class Meta:
        proxy = True
   #     permissions = (
   #         ('accept_registrationprofile', _('Can accept registration profile')),
   #         ('reject_registrationprofile', _('Can reject registration profile')),
   #     )
   # 
   # @classmethod
   # def _get_administers(cls):
   #     PERMISSIONS = ['accept_registrationprofile', 'reject_registrationprofile']
   #     groups = Group.objects.filter(permissions__codename__in=PERMISSIONS).distinct()
   #     group_pks = [g.pk for g in groups.all()]
   #     users = User.objects.filter(
   #             Q(user_permissions__codename__in=PERMISSIONS) |
   #             Q(groups__pk__in = group_pks)).distinct()
   #     return users

    def _create_email(self, action, site, extra_context=None):
        ACCEPTED_ACTIONS = (
                'acception', 'rejection', 'notification', 'activation', 'activated',
            )
        if action not in ACCEPTED_ACTIONS:
            raise AttributeError("'action' must be in '%s'" % ACCEPTED_ACTIONS)

        from_email = settings.DEFAULT_FROM_EMAIL

        context = {
                'site': site,
                'user': self.user,
                'registration_profile': self,
            }
        if extra_context:
            context.update(extra_context)

        template_name = 'registration/%s_email_subject.txt' % action
        subject = render_to_string(template_name, context)
        subject = ''.join(subject.splitlines())

        template_name = 'registration/%s_email.txt' % action
        message = render_to_string(template_name, context)

        return {'subject': subject, 'message': message, 'from_email': from_email}

    def send_acception_email(self, site):
        email = self._create_email('acception', site)
        self.user.email_user(**email)

    def send_rejection_email(self, reason, site):
        extra_context = {'reason': reason}
        email = self._create_email('rejection', site, extra_context)
        self.user.email_user(**email)

    def send_notification_email(self, site):
        email = self._create_email('rejection', site)
        for administer in self._get_administers().all():
            administer.user.email_user(**email)

    def send_activation_email(self, site, password=None):
        extra_context = {
                'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            }
        if password:
            extra_context['password'] = password
        email = self._create_email('activation', site, extra_context)
        self.user.email_user(**email)

    def send_activated_email(self, site, password=None):
        extra_context = {}
        if password:
            extra_context['password'] = password
        email = self._create_email('activated', site, extra_context)
        self.user.email_user(**email)

    def activation_key_expired(self):
        if self.activation_key == self.UNTREATED:
            return False
        elif self.activation_key == self.REJECTED:
            return True
        return super(RegistrationProfile, self).activation_key_expired()
    activation_key_expired.boolean = True
