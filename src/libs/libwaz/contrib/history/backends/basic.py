# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.db.models import signals
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType

from base import BaseHistoryBackend
from ..models import Timeline

from datetime import datetime, timedelta

class BasicHistoryBackend(BaseHistoryBackend):
    
    def _validate(self, action, url, label, user):
        if not url or not label:
            return False
        now = datetime.now()
        span = timedelta(seconds=300)
        qs = Timeline.objects.filter(url=url)
        if qs.filter(action=action, created_at__gt=(now-span)).exists():
            return False
        if action == 'update' and (qs.filter(action='create').count() - qs.filter(action='delete').count()) == 0:
            action = 'create'
        return (action, url, label, user)
    def _post_save_callback(self, instance, created, **kwargs):
        self.autodiscover(instance, 'create' if created else 'update')
    def _pre_delete_callback(self, instance, **kwargs):
        self.autodiscover(instance, 'delete')
        
    def setUp(self, model):
        signals.post_save.connect(self._post_save_callback, sender=model)
        # signals.pre_delete.connect(self._pre_delete_callback, sender=model)
    def tearDown(self, model):
        signals.post_save.disconnect(self._post_save_callback, sender=model)
        # signals.pre_delete.disconnect(self._pre_delete_callback, sender=model)
    
    
    def autodiscover(self, instance, action, url=None, label=None, user=None):
        if url is None:
            url = self._get_url_from_instance(instance)
        if label is None:
            label = self._get_label_from_instance(instance)
        if user is None:
            user = self._get_user_from_instance(instance)
        if user == 'anonymous' or isinstance(user, AnonymousUser):
            user = None
        if action is True:
            action = 'create'
        elif action is False:
            action = 'update'
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
