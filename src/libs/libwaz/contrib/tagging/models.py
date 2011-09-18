# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from exceptions import DuplicateError, DeletingFrozenTagError
from utils import parse_tag_input

class TagManager(models.Manager):
    u"""Model manager for tag model"""
    
    def add_tag(self, obj, label, ignore_duplicate=True):
        u"""Add `label` tag to the obj and return TaggedItem instance"""
        ctype = ContentType.objects.get_for_model(obj)
        tag = Tag.objects.get_or_create(label=label)[0]
        tagged_item, created, = TaggedItem.objects.get_or_create(tag=tag, content_type=ctype, object_id=obj.pk)
        if not ignore_duplicate and not created:
            raise DuplicateError(_('`%s` tag is already related to the object.') % label)
        return tagged_item

    def update_tags(self, obj, labels):
        u"""Update tags of the obj by `labels`"""
        ctype = ContentType.objects.get_for_model(obj)
        current_tags = list(self.filter(items__content_type=ctype, items__object_id=obj.pk))
        updated_tag_labels = parse_tag_input(labels)
        # Remove all tags not in updated_tag_labels
        tags_for_removal = [tag for tag in current_tags if tag.label not in updated_tag_labels]
        if len(tags_for_removal):
            TaggedItem._default_manager.filter(
                content_object=obj,
                tag__in=tags_for_removal).delete()
        # Append new tags
        current_tag_labels = [tag.label for tag in current_tags]
        for tag_label in updated_tag_labels:
            if not tag_label in current_tag_labels:
                tag = self.get_or_create(label=tag_label)[0]
                TaggedItem._default_manager.create(tag=tag, content_object=obj)
    
    def remove_tag(self, obj, label):
        u"""Remove `label` tag from the obj and return TaggedItem removed.
        
        Caution:
            TaggedItem instance returned is removed. That's mean the instance
            DOES NOT have `pk`
        """
        tagged_item = TaggedItem.objects.get_for_object(obj).get(tag__label=label)
        if tagged_item.frozen:
            raise DeletingFrozenTagError(_('Unable to remove `%s` tag while it is frozen.') % label)
        tagged_item.delete()
        if tagged_item.tag.items.count() == 0:
            tagged_item.tag.delete()
        return tagged_item

    def freeze_tag(self, obj, label, status=None):
        u"""Freeze or thaw `label` tag related to the obj.
        
        Options:
            status    - give `freeze` when you want to freeze tag
                        and give `thaw` when you want to thaw tag.
                        if it set `None` that's mean toggle status
                        of tag.
        """
        tagged_item = TaggedItem.objects.get_for_object(obj).get(tag__label=label)
        if status == 'thaw' or (tagged_item.frozen and not status):
            tagged_item.frozen = False
        elif status == 'freeze' or (not tagged_item.frozen and not status):
            tagged_item.frozen = True
        tagged_item.save()
        return tagged_item
        
    def get_for_model(self, model):
        u"""Return tags related to the model"""
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(items__content_type=ctype).distinct()
    
    def get_for_object(self, obj):
        u"""Return tags related to the obj"""
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(items__content_type=ctype, items__object_id=obj.pk).distinct().order_by('items__order')
    
class TaggedItemManager(models.Manager):
    u"""Model manager for TaggedItem"""
    
    def get_for_model(self, model):
        u"""Return tagged_items related to the model"""
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(content_type=ctype).distinct()
    
    def get_for_object(self, obj):
        u"""Return tagged_items related to the obj"""
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ctype, object_id=obj.pk).distinct().order_by('order')

class Tag(models.Model):
    u"""Model of tag"""
    label       = models.CharField(_('label'), max_length=settings.MAX_TAG_LENGTH, unique=True, db_index=True)
    
    objects     = TagManager()
    
    class Meta:
        ordering            = ('label',)
        verbose_name        = _('tag')
        verbose_name_plural = _('tags')

    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('tagging-tag-detail', (), {'slug': self.label})

class TaggedItem(models.Model):
    u"""Model of tagged item"""
    tag             = models.ForeignKey(Tag, verbose_name=_('tag'), related_name='items')
    content_type    = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_id       = models.PositiveIntegerField(_('object ID'))
    content_object  = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    frozen          = models.BooleanField(_('frozen status'), default=False)
    order           = models.IntegerField(_('order'), default=-1, blank=True)
    
    objects = TaggedItemManager()
    
    class Meta:
        ordering            = ('order',)
        unique_together     = (('tag', 'content_type', 'object_id'),)
        verbose_name        = _('tagged item')
        verbose_name_plural = _('tagged items')

    def __unicode__(self):
        return self.tag.__unicode__()

    def save(self, *args, **kwargs):
        if self.order == -1:
            queryset = TaggedItem.objects.get_for_object(self.content_object)
            if queryset.count() > 0:
                dict = queryset.aggregate(max=Max('order'))
                self.order = dict['max']+1
            else:
                self.order = 0
        super(TaggedItem, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        u"""Return permalink of object related."""
        return self.content_object.get_absolute_url()
    
    def json(self):
        u"""Return dictionary object for json"""
        return {
            'pk':       self.tag.pk,
            'label':    self.tag.label,
            'url':      self.tag.get_absolute_url(),
            'order':    self.order,
            'frozen':   self.frozen,
        }
