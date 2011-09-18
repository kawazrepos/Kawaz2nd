# -*- coding: utf-8 -*-
#
# @date:        2010/09/26
# @author:    alisue
#
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

class Trackback(models.Model):
    """
    A received Trackback or Pingback
    As the model is pretty similar to django.contrib.comments.FreeComment
    django-trackback may switch to using it in the future.
    
    """
    url             = models.URLField(verify_exists=not settings.DEBUG)
    # Note that when you're using the single-threaded development server, 
    # validating a URL being served by the same server will hang. 
    # This should not be a problem for multithreaded servers.
    title           = models.CharField(max_length=255, blank=True)
    blog_name       = models.CharField(max_length=255, blank=True)
    excerpt         = models.TextField(blank=True)
    
    content_type    = models.ForeignKey(ContentType,
        verbose_name=_('content type'),
        related_name="content_type_set_for_%(class)s",
        editable=False)
    object_id       = models.PositiveIntegerField(_('object ID'), blank=True, editable=False)
    content_object  = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")

    remote_ip       = models.IPAddressField(editable=False)
    site            = models.ForeignKey(Site, editable=False)
    
    submit_date     = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name        = _(u"trackback")
        verbose_name_plural = _(u"trackbacks")
    
    def __unicode__(self):
        return u"Trackback from `%s`" % self.url
    
