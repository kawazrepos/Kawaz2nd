# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from django.utils.translation import ugettext_lazy as _

from sites import site

class Timeline(models.Model):
    u"""Django model's history model"""
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id       = models.PositiveIntegerField(_('object_id'), null=True)
    content_object  = GenericForeignKey()
    
    action          = models.CharField(_('action'), max_length=30)
    url             = models.URLField(_('URL'))
    label           = models.CharField(_('label'), max_length=255)
    user            = models.ForeignKey(User, verbose_name=_('user'), null=True, blank=True)
    created_at      = models.DateTimeField(_('create at'), auto_now_add=True)
    
    class Meta:
        ordering            = ['-created_at']
        verbose_name        = _('timeline')
        verbose_name_plural = _('timelines')
    
    def get_absolute_url(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not settings.HISTORY_ENABLE:
            return None
        return super(Timeline, self).save(*args, **kwargs)
    
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
