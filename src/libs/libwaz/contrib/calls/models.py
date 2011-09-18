# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from django.utils.translation import ugettext_lazy as _

from sites import site

class Call(models.Model):
    u"""Call object that particular user call other particular user"""
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id       = models.PositiveIntegerField(_('object id'), null=True)
    content_object  = GenericForeignKey()
    
    url             = models.URLField(_('URL'))
    label           = models.CharField(_('label'), max_length=255)
    user_to         = models.ForeignKey(User, related_name="called_from")
    user_from       = models.ForeignKey(User, related_name="called_to", editable=False, null=True)
    read            = models.BooleanField(_('read flag'), default=False)
    created_at      = models.DateTimeField(_('datetime created'), auto_now_add=True)
    updated_at      = models.DateTimeField(_('datetime modified'), auto_now=True)
    
    class Meta:
        ordering            = ('-created_at',)
        unique_together     = ('url', 'user_to',)
        verbose_name        = _('call')
        verbose_name_plural = _('calls')
    
    @property
    def _backend(self):
        if hasattr(self, '_backend_cache'):
            return self._backend_cache
        model = self.content_type.model_class()
        self._backend_cache = site.get_backend(model)
        return self._backend_cache
        
    def get_message(self):
        u"""
        Get message for this timeline
        """
        #if hasattr(self, '_message_cache'):
        #    return self._message_cache
        self._message_cache = self._backend.get_message(self)
        return self._message_cache