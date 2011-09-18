# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ..models import Call

class BaseCallsBackend(object):
    def setUp(self, model):
        u"""Setup backend called when backend is registered."""
        pass
    def tearDown(self, model):
        u"""Tear down backend callend when backend is unregistered."""
        pass
    
    def _get_url_from_instance(self, instance):
        u"""Get url from instance dependent on `get_absolute_url` method"""
        if instance and hasattr(instance, 'get_absolute_url'):
            return instance.get_absolute_url()
        return None
    def _get_label_from_instance(self, instance):
        u"""Get label from instance dependent on `__unicode__` method"""
        if instance and hasattr(instance, '__unicode__'):
            return instance.__unicode__()
        return None
    def _get_user_from_instance(self, instance):
        u"""Get user from instance dependent on `CALLS_USER_ATTRS` on settings.py"""
        if not instance:
            return None
        for attr in settings.CALLS_USER_ATTRS:
            if hasattr(instance, attr):
                return getattr(instance, attr)
        return None
    
    def validate(self, url, label, user_to, user_from):
        u"""Validation the value and return cleaned values when validate true. Subclass should override this method when custome validation is needed."""
        if not (url and label and user_to and user_from):
            return False
        elif not isinstance(user_to, User) or not isinstance(user_from, User):
            return False
        elif user_to == user_from:
            return False
        return url, label, user_to, user_from
    
    def _get_user_name_with_permalink(self, user):
        u"""Get user name with permalink from user instance"""
        if hasattr(user, 'get_profile'):
            kwargs = {
                'href':     user.get_profile().get_absolute_url(),
                'title':    user.get_profile().__unicode__(),
                'label':    user.get_profile().__unicode__(),
            }
        else:
            kwargs = {
                'href':     user.get_absolute_url(),
                'title':    user.__unicode__(),
                'label':    user.__unicode__(),
            }
        return mark_safe(u"""<a href="%(href)s" title="%(title)s">%(label)s</a>""" % kwargs)
    def get_user_to(self, call):
        u"""Get user name with permalink from `user_to` attribute of call."""
        return self._get_user_name_with_permalink(call.user_to)
        
    def get_user_from(self, call):
        u"""Get user name with permalink from `user_from` attribute of call."""
        if call.user_from:
            return self._get_user_name_with_permalink(call.user_from)
        else:
            return _("Anonymous User")
        
    def get_label(self, call):
        u"""Get label with permalink"""
        kwargs = {
            'href':     call.url,
            'label':    call.label,
        }
        return mark_safe(u"""<a href="%(href)s">%(label)s</a>""" % kwargs)
    
    def autodiscover(self, instance, created, url=None, label=None, user_to=None, user_from=None, read=False):
        u"""Automatically discover call from instance. Subclass must override this method."""
        raise NotImplementedError
    
    def get_message(self, call):
        u"""Get message from call. Subclass must override this method."""
        raise NotImplementedError
    
class BasicCallsBackend(BaseCallsBackend):
    u"""Basic calls backend. autodiscover from instance and get message with MESSAGE attribute of backend."""
    
    # Override the attribute below in subclass.
    MESSAGE = _('Your name is called at "%(label)s" by %(user_from)s.')
    
    def _post_save_callback(self, sender, instance, created, **kwargs):
        u"""Callend when instance is saved. Subclass should override this method when controlling creation of call is needed."""
        self.autodiscover(instance=instance, created=created)
    
    def _pre_delete_callback(self, sender, instance, **kwargs):
        u"""Called when instance is deleted. Subclass should override this method when controlling deletation of call is needed."""
        url = instance.get_absolute_url()
        calls = Call.objects.filter(url=url)
        for call in calls:
            call.read = True
            call.save()
            
    def setUp(self, model):
        post_save.connect(self._post_save_callback, sender=model)
        pre_delete.connect(self._pre_delete_callback, sender=model)
    def tearDown(self, model):
        post_save.disconnect(self._post_save_callback, sender=model)
        pre_delete.disconnect(self._pre_delete_callback, sender=model)
        
    def autodiscover(self, instance, created, url=None, label=None, user_to=None, user_from=None, read=None):
        u"""Automatically discover call from instance. `user_to` argument is required otherwise call never be created."""
        if not instance or not user_to:
            return
        url = url or self._get_url_from_instance(instance)
        label = label or self._get_label_from_instance(instance)
        user_from = user_from or self._get_user_from_instance(instance)
        
        cleaned_data = self.validate(url, label, user_to, user_from)
        if not cleaned_data:
            return
        url, label, user_to, user_from = cleaned_data
        ct = ContentType.objects.get_for_model(instance)
        if Call.objects.filter(url=url, user_to=user_to).exists():
            call = Call.objects.get(url=url, user_to=user_to)
            call.content_type = ct
        else:
            call = Call.objects.create(url=url, user_to=user_to, content_type=ct)
        call.object_id = instance.pk
        call.label = label
        call.user_to = user_to
        call.user_from = user_from
        call.read = read or call.read
        call.save()
    
    def get_message(self, call, message=None, user_to=None, user_from=None, label=None):
        u"""Get message with `MESSAGE` attribute of backend. Override it when you want to configure the message.
        
        Parameters given to `MESSAGE`:
            user_to:    user name with permalink from `user_to` attribute of call
            user_from:  user name with permalink from `user_from` attribute of call
            label:      label with permalink from `label`, `url` attribute of call
        """
        kwargs = {
            'user_to': user_to or self.get_user_to(call),
            'user_from': user_from or self.get_user_from(call),
            'label': label or self.get_label(call),
        }
        message = message or self.MESSAGE
        return mark_safe(message % kwargs)