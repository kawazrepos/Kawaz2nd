# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from basic import BasicHistoryBackend
from ..models import Timeline

class CommentHistoryBackend(BasicHistoryBackend):
    def get_message(self, timeline):
        u"""
        get message for timeline object from content_object with permalinks
        """
        kwargs = {
            'user':     self.get_user(timeline),
            'label':    self.get_label(timeline),
        }
        if timeline.action == 'create':
            return mark_safe(_(u"""%(user)s has comment to '%(label)s'""") % kwargs)
        elif timeline.action == 'update':
            return mark_safe(_(u"""%(user)s update a comment of '%(label)s'""") % kwargs)
        return mark_safe(_(u"""%(user)s delete a comment of '%(label)s'""") % kwargs)
    
    def autodiscover(self, instance, action, url=None, label=None, user=None):
        if url is None:
            url = self._get_url_from_instance(instance)
        if label is None:
            label = self._get_label_from_instance(instance.content_object)
        if user is None:
            user = instance.user
        if user == 'anonymous' or isinstance(user, AnonymousUser):
            user = None
        if action is True:
            action = 'create'
        elif action is False:
            action = 'update'
        if action == 'update' and instance.is_removed:
            action = 'delete'
        cleaned_data = self._validate(action, url, label, user)
        if cleaned_data:
            action, url, label, user = cleaned_data
            timeline = Timeline.objects.create(
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
                action=action,
                url=url,
                label=label,
                user=user,
            )
            return timeline
        else:
            return None