# -*- coding: utf-8 -*-
#
# Created:        2010/11/08
# Author:        alisue
#
from django.conf import settings
from django.db import models
from django.db import transaction
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

import random

from registration.models import RegistrationManager as _RegistrationManager
from registration.models import RegistrationProfile as _RegistrationProfile

class RegistrationManager(_RegistrationManager):
    
    def activate_user(self, activation_key, site, send_email=True):
        user = super(RegistrationManager, self).activate_user(activation_key)
        if user and send_email:
            registration_profile= self.get(user=user)
            registration_profile.send_activated_email(site)
        return user
    
    def approve_user(self, registration_profile, site, send_email=True):
        if not registration_profile.user.is_active and registration_profile.status == 'waiting':
            user = registration_profile.user
            registration_profile.status = 'approved'
            registration_profile.save()
            if send_email:
                registration_profile.send_activation_email(site)
            return user
        return False
    
    def reject_user(self, registration_profile, site, send_email=True):
        if not registration_profile.user.is_active:
            if send_email:
                registration_profile.send_rejection_email(site)
            user = registration_profile.user
            user.delete()
            return user
        return False
    
    @transaction.commit_on_success
    def create_inactive_user(self, username, email, password,
                             remarks, site, send_email=True):
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user, remarks)

        if send_email:
            registration_profile.send_registration_email(site, password)
            registration_profile.send_notification_email_to_managers(site)
            
        return new_user
    
    def create_profile(self, user, remarks):
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt+user.username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key,
                           remarks=remarks)
            
class RegistrationProfile(_RegistrationProfile):
    STATUS = (
        ('waiting',     _('Waiting')),
        ('approved',    _('Approved')),
    )
    status      = models.CharField(_('status'), max_length=10, choices=STATUS, default='waiting', editable=False)
    remarks     = models.TextField(_('remarks'), blank=True)
    
    objects     = RegistrationManager()
    
    class Meta:
        permissions = (
            ('view_registrationprofile',    u"Can view registration profile"),
            ('approve_registrationprofile', u"Can approve registration profile"),
            ('reject_registrationprofile',  u"Can reject registration profile"),
        )
        verbose_name        = _('registration profile')
        verbose_name_plural = _('registration profiles')
        
    def __unicode__(self):
        return self.user.username
    
    def send_registration_email(self, site, password=None):
        ctx_dict = {'site': site, 'user': self.user, 'registration_profile': self, 'password': password}
        
        subject = render_to_string('registration/registration_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/registration_email.txt',
                                   ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        
    def send_rejection_email(self, site):
        ctx_dict = {'site': site, 'user': self.user, 'registration_profile': self}
        
        subject = render_to_string('registration/rejection_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/rejection_email.txt',
                                   ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    
    def send_activated_email(self, site):
        ctx_dict = {'site': site, 'user': self.user, 'registration_profile': self}
        
        subject = render_to_string('registration/activated_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/activated_email.txt',
                                   ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    
    def send_notification_email_to_managers(self, site):
        PERMISSIONS =['view_registrationprofile', 'approve_registrationprofile', 'reject_registrationprofile']
        manager_groups = Group.objects.filter(permissions__codename__in=PERMISSIONS).distinct()
        managers = User.objects.exclude(is_active=False).exclude(email='')
        managers = managers.filter(
            Q(user_permissions__codename__in=PERMISSIONS) | 
            Q(groups__pk__in=[group.pk for group in manager_groups.all()])).distinct()
        
        ctx_dict = {'site': site, 'user': self.user, 'registration_profile': self}
        
        subject = render_to_string('registration/on_registration_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/on_registration_email.txt',
                                   ctx_dict)
    
        for manager in managers.all():
            manager.email_user(subject, message)