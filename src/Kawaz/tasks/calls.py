# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/30
#
from django.db.models.signals import pre_delete, m2m_changed
from django.contrib.auth.models import User
from libwaz.contrib.calls import site
from libwaz.contrib.calls.models import Call
from libwaz.contrib.calls.backends import BasicCallsBackend

from models import Task

class TaskCallsBackend(BasicCallsBackend):
    MESSAGE = u"%(user_from)sからタスク「%(label)s」の依頼があります"
    REJECTED_MESSAGE = u"%(user_from)sからタスク「%(label)s」の再作業要請があります"
    
    def _post_save_callback(self, sender, instance, created, **kwargs):
        if instance.status == 'rejected':
            for user_to in instance.owners.all():
                self.autodiscover(instance, created, user_to=user_to)
        else:
            url = instance.get_absolute_url()
            calls = Call.objects.filter(url=url)
            for call in calls:
                call.read = True
                call.save()
                
    def _m2m_changed_callback(self, sender, instance, action, reverse, model, pk_set, **kwargs):
        if instance.pub_state == 'draft' or action != 'post_add' or model != User:
            return
        users = User.objects.filter(pk__in=pk_set)
        for user_to in users:
            self.autodiscover(instance, created=False, user_to=user_to, read=False)
        
    def _pre_delete_callback(self, sender, instance, **kwargs):
        u"""Called when instance is deleted. Subclass should override this method when controlling deletation of call is needed."""
        url = instance.get_absolute_url()
        calls = Call.objects.filter(url=url)
        for call in calls:
            call.read = True
            call.save()
            
    def setUp(self, model):
        m2m_changed.connect(self._m2m_changed_callback, sender=model.owners.through)
        pre_delete.connect(self._pre_delete_callback, sender=model)
    def tearDown(self, model):
        m2m_changed.disconnect(self._m2m_changed_callback, sender=model.owners.through)
        pre_delete.disconnect(self._pre_delete_callback, sender=model)
    
    def get_message(self, call):
        if call.content_object.status == 'reject':
            message = self.REJECTED_MESSAGE
        else:
            message = self.MESSAGE
        return super(TaskCallsBackend, self).get_message(call, message=message)
    
site.register(Task, TaskCallsBackend)