# -*- coding: utf-8 -*-
#    
#    
#    created by giginet on 2011/07/20
#
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

class StarManager(models.Manager):
    u"""Model manager for star model"""
    def add_star(self, obj, user, comment=None, color=0):
        u"""Add star to the obj with 'comment' and 'color' and return the created star"""
        ctype = ContentType.objects.get_for_model(obj)
        tag = Tag.objects.get_or_create(label=label)[0]
        star, created = Star.objects.create(author=user, color=color, content_type=ctype, object_id=obj.pk, comment=comment)
        if created:
            return star
        return None
     
    def get_for_model(self, model):
        u"""Return stars related to the model"""
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()
    
    def get_for_object(self, obj):
        u"""Return stars related to the obj"""
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(items__content_type=ctype, items__object_id=obj.pk).distinct()

class Star(models.Model):
    u"""model of star"""
    #required
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_id       = models.PositiveIntegerField(_('object ID'))
    content_object  = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    color           = models.IntegerField(verbose_name=_('color'), default=0)
    #not required
    comment         = models.CharField(_('comment'), max_length=255)
    #uneditable
    author          = models.ForeignKey(User, verbose_name=_('user'), related_name='stars', editable=False)
    created_at      = models.DateTimeField(_('create at'), auto_now_add=True)
    
    objects         = StarManager()
    
    class Meta:
        ordering            = ('created_at',)
        verbose_name        = _('star')
        verbose_name_plural = _('stars')
        
    def __unicode__(self):
        return u'%s %s' % (self.comment, self.content_object)
    
    def json(self):
        u"""Return dictionary object for json"""
        return {
            'pk':        self.pk,
            'author':    self.author,
            'comment':   self.comment,
            'created_at':self.created_at,
        }